import django
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import Http404, StreamingHttpResponse
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic import View
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .default_settings import SURVEY_CONFIG
from .auditors import NAME_TO_AUDITOR
from .steps import NAME_TO_STEP
from .models import Task, TaskInteraction, Token

from .renderers import XMLBodyRenderer


# The authentication system in DRF is intimately tied to Django's user model,
# So we're basically taking a pass on being involved on that and using this
# authentication class as a no-op
class NonAuthentication(BaseAuthentication):
    def authenticate(self, request):
        pass


class RecordSubmission(APIView):
    authentication_classes = (NonAuthentication,)
    permission_classes = (AllowAny,)
    NAME_TO_MODEL_MAPPING = None
    ALREADY_SUBMITTED_VALIDATION_MESSAGE = _('Data already submitted for this task')
    DATA_KEY = None

    def save_data_to_mapped_models(self, data,
                                   task_interaction_model):
        model_to_name = {v: k for k, v in self.NAME_TO_MODEL_MAPPING.items()}
        associated_models = self.get_associated_models(task_interaction_model)
        for model in associated_models:
            model_class_name = type(model).__name__
            try:
                model_data = data[model_to_name[model_class_name]]
            except KeyError:
                raise ValidationError(_('Missing or invalid data'
                                        'from one or more steps or auditors'))
            model.handle_submission_data(model_data, task_interaction_model)

    def get_task_interaction(self, interaction_pk, request):
        """
        Helper function to get a task interaction from a potentially invalid
        string representing interaction_pk and request.
        Must be called from within a transaction because it locks the task
        interaction using "select_for_update" method on the queryset.

        If string is invalid it returns None.
        """
        task_interaction = None
        try:
            if 'token' not in request.data:
                return None
            token = Token.objects.get(token=request.data['token'])
            task_interaction = TaskInteraction.objects \
                .select_for_update() \
                .select_related('task') \
                .get(pk=int(interaction_pk), token=token)
        except ValueError:
            pass
        except TaskInteraction.DoesNotExist:
            pass
        except Token.DoesNotExist:
            pass

        return task_interaction

    def process_submission(self, submission_data, task_interaction):
        if self.associated_models_have_data(task_interaction):
            raise ValidationError(self.ALREADY_SUBMITTED_VALIDATION_MESSAGE)

        self.save_data_to_mapped_models(submission_data[self.DATA_KEY],
                                        task_interaction)

    def get_associated_models(self, task_interaction):
        """
        Get models of steps or auditors that apply to the task
        linked to by task_interaction
        """
        associated_models = []

        for model_name in self.NAME_TO_MODEL_MAPPING.values():
            model = apps.get_model('survey', model_name)
            associated_models.extend(model.objects.filter(task=task_interaction.task))

        return associated_models

    def associated_models_have_data(self, task_interaction):
        """
        Find out if the models associated with a task_interaction
        already have data instances. This serves to show us whether there has
        already been a submission or not
        """
        associated_models = self.get_associated_models(task_interaction)
        for model in associated_models:
            if model.has_data_for_task_interaction(task_interaction):
                return True

        return False

    def post(self, request, **kwargs):
        with transaction.atomic():
            task_interaction_model = self.get_task_interaction(kwargs['pk'], request)
            if not task_interaction_model:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not task_interaction_model.task.published:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                self.process_submission(request.data, task_interaction_model)
                return Response(status=status.HTTP_201_CREATED)
            except ValidationError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except django.core.exceptions.ValidationError:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class StepSubmission(RecordSubmission):
    NAME_TO_MODEL_MAPPING = NAME_TO_STEP
    DATA_KEY = 'steps'

    def process_submission(self, submission_data, task_interaction):
        if task_interaction.task.external:
            raise ValidationError(_('Submitting steps on an internal HIT'))

        super().process_submission(submission_data, task_interaction)


class AuditorSubmission(RecordSubmission):
    NAME_TO_MODEL_MAPPING = NAME_TO_AUDITOR
    DATA_KEY = 'auditors'


class CreateTaskInteractionView(APIView):
    authentication_classes = (NonAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        if type(request.data) is not dict or 'task_pk' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            task = Task.objects.get(pk=int(request.data['task_pk']))
        except Task.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not task.published:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if 'token' in request.data:
            try:
                token = Token.objects.get(token=request.data['token'])
            except Token.DoesNotExist:
                token = Token.objects.create()
            if not token.valid:
                token = Token.objects.create()
        else:
            token = Token.objects.create()

        task_interaction = TaskInteraction.objects.create(task=task,
                                                          token=token)

        return Response(data={'task_interaction': task_interaction.pk,
                              'auditor_submission_url': request.build_absolute_uri(
                                  reverse('survey:auditor_submission',
                                          kwargs={'pk': task_interaction.pk})),
                              'step_submission_url': request.build_absolute_uri(
                                  reverse('survey:step_submission',
                                          kwargs={'pk': task_interaction.pk})),
                              'token': token.token},
                        status=status.HTTP_201_CREATED)


class TaskView(View):
    def get(self, request, **kwargs):
        TASK_NOT_FOUND = Http404(_('No such task'))
        try:
            task = Task.objects.get(pk=kwargs['pk'])
        except Task.DoesNotExist:
            raise TASK_NOT_FOUND

        if task.external or not task.published:
            raise TASK_NOT_FOUND

        # TODO: Find a way to cut down on the number of queries these loops will have to make

        steps = []
        for step_model_name in NAME_TO_STEP.values():
            step_model = apps.get_model('survey', step_model_name)
            steps.extend(step_model.objects.filter(task=task))
        steps.sort(key=lambda x: x.step_num)

        # serves to only get one instance of each script
        # needed for steps, since it is valid
        # for a user to have multiple steps (e.g. multiple choice)
        step_script_locations = list(
            set([step.script_location for step in steps]))

        auditor_uris = []
        for auditor_model_name in NAME_TO_AUDITOR.values():
            auditor_model = apps.get_model('survey', auditor_model_name)
            try:
                auditor = auditor_model.objects.get(task=task)
                auditor_uris.append(static(auditor.script_location))
            except auditor_model.DoesNotExist:
                pass

        fetch_interaction_endpoint = reverse('survey:create_interaction')

        return TemplateResponse(
            request,
            task.survey_wrap_template,
            status=status.HTTP_200_OK,
            context={'steps': steps,
                     'task': task,
                     'step_script_locations': step_script_locations,
                     'auditor_uris': auditor_uris,
                     'fetch_interaction_endpoint': fetch_interaction_endpoint,
                     'token_name': SURVEY_CONFIG['TOKEN_NAME']},
        )


class TasksExport(LoginRequiredMixin, APIView):
    NUMBER_RECORDS_PER_QUERY = 5 * 10 ** 2
    XML_OPENING_LINE = '<?xml version="1.0" encoding="UTF-8"?>'

    def _get_related_auditors(self, task):
        auditors = dict()
        for auditor_name, auditor in NAME_TO_AUDITOR.items():
            auditor = apps.get_model('survey', auditor)
            try:
                auditors[auditor_name] = auditor.objects.get(task=task)
            except auditor.DoesNotExist:
                pass
        return auditors

    def _get_related_steps(self, task):
        steps = dict()
        for step_name, step_model in NAME_TO_STEP.items():
            step = apps.get_model('survey', step_model)
            step_models = step.objects.filter(task=task)
            if step_models.count() > 0:
                steps[step_name] = step_models
        return steps

    def _get_related_tokens(self, task):
        # return tokens where the token is linked to at least one
        # task interaction that is in turn linked to task
        #
        # Pseudo-SQL:
        # SELECT DISTINCT TOKENS.<all_fields>
        # FROM TOKENS
        # INNER JOIN TASK_INTERACTIONS
        # ON TASK_INTERACTIONS.TOKEN = TOKENS.PK
        # WHERE TASK_INTERACTIONS.TASK = <task>
        task_interactions = TaskInteraction.objects.filter(task=task)
        return Token.objects.filter(taskinteraction__in=task_interactions).distinct()

    def _render_auditors_meta_xml(self, request, task):
        auditors = self._get_related_auditors(task)

        serialized_auditors = []
        for auditor_name, auditor in auditors.items():
            serialized_auditor = auditor.serialize_info_to_dict()
            serialized_auditor['name'] = auditor_name
            serialized_auditors.append(serialized_auditor)

        # assemble a string, our auditors xml
        auditors_xml = XMLBodyRenderer(root_tag_name='auditors_meta')
        return auditors_xml.render(serialized_auditors)

    def _render_steps_meta_xml(self, request, task):
        steps = self._get_related_steps(task)

        serialized_steps = []
        for step_name, step_list in steps.items():
            serialized_step_models = \
                {'instances': [step.serialize_info_to_dict() for step in
                               step_list],
                 'name': step_name}
            serialized_steps.append(serialized_step_models)

        steps_xml = XMLBodyRenderer(root_tag_name='steps_meta')
        return steps_xml.render(serialized_steps)

    def _render_tokens_xml(self, request, task):
        tokens = self._get_related_tokens(task)

        serialized_tokens = [token.serialize_info_to_dict() for token in tokens]

        tokens_xml = XMLBodyRenderer(root_tag_name='tokens_meta')
        return tokens_xml.render(serialized_tokens)

    def _render_task_meta_xml(self, request, task):
        auditors_xml = self._render_auditors_meta_xml(request, task)
        steps_xml = self._render_steps_meta_xml(request, task)
        tokens_xml = self._render_tokens_xml(request, task)
        renderer = XMLBodyRenderer(root_tag_name='task_meta')
        task_xml = renderer.render(task.serialize_info_to_dict())
        return ''.join([task_xml, auditors_xml, steps_xml, tokens_xml])

    def _get_auditors_dict(self, interaction, auditors):
        auditors_serialized = dict()
        for auditor_name, auditor in auditors.items():
            serialized_data = auditor.serialize_data(interaction)
            auditors_serialized[auditor_name] = serialized_data
        return auditors_serialized

    def _get_steps_dict(self, interaction, steps):
        steps_serialized = dict()
        for step_name, step_list in steps.items():
            serialized_steps = []
            for step in step_list:
                serialized_steps.append({'pk': step.pk,
                                         'data': step.serialize_data(interaction)})
            steps_serialized[step_name] = serialized_steps
        return steps_serialized

    def _render_task_interactions(self, request, task_interactions):
        if task_interactions.count() == 0:
            return ''

        auditors = self._get_related_auditors(task_interactions[0].task)
        steps = self._get_related_steps(task_interactions[0].task)

        # TODO: Implement prefetching to keep this loop from making multiple queries per interaction
        renderer = XMLBodyRenderer(root_tag_name='interaction')
        interactions = []
        for interaction in task_interactions:
            serialized = {'meta': interaction.serialize_info_to_dict()}
            serialized['auditors'] = self._get_auditors_dict(interaction,
                                                             auditors)
            serialized['steps'] = self._get_steps_dict(interaction,
                                                       steps)
            interactions.append(renderer.render(serialized))
        return ''.join(interactions)

    def _get_response_iterator(self, request, tasks):
        yield self.XML_OPENING_LINE
        for task in tasks:
            yield '<task>'
            yield '<pk>%d</pk>' % task.pk
            yield '<meta>'
            yield self._render_task_meta_xml(request, task)
            yield '</meta>'
            yield '<task_interactions>'
            paginator = Paginator(task.taskinteraction_set.all(),
                                  self.NUMBER_RECORDS_PER_QUERY)
            # annoyingly, Django's Paginator was only designed with templates
            # in mind, despite its utility for breaking up large queries.
            # The generator expression
            # (paginator.page(n).object_list for n in paginator.page_range)
            # creates a generator of page sized object lists
            for task_interactions in (paginator.page(n).object_list for n in
                                      paginator.page_range):
                yield self._render_task_interactions(request,
                                                     task_interactions)
            yield '</task_interactions>'
            yield '</task>'

    def get(self, request, primary_keys=None):
        if not primary_keys:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            primary_keys = [int(n) for n in primary_keys.split(',')]
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # "trust but verify"
        tasks = Task.objects.filter(pk__in=primary_keys)
        if tasks.count() != len(primary_keys):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for task in tasks:
            if request.user not in task.owners.all()\
                    and not request.user.is_superuser:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        response_iterator = self._get_response_iterator(request, tasks)
        return StreamingHttpResponse(response_iterator,
                                     content_type='text/xml')


class ThanksView(TemplateView):
    template_name = 'survey/thanks.html'
