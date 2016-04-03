from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.http import Http404, StreamingHttpResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from .auditors import NAME_TO_AUDITOR
from .steps import NAME_TO_STEP
from .models import Task, TaskInteraction


# TODO: Authentication
from survey.renderers import XMLBodyRenderer


class RecordSubmission(APIView):
    def save_data_to_mapped_models(self, data, map,
                                   task_interaction_model):
        task = task_interaction_model.task
        for name, model_data in data.items():
            associated_models = apps.get_model('survey', map[name]) \
                .objects.filter(task=task)
            for model in associated_models:
                model.handle_submission_data(model_data,
                                             task_interaction_model)

    def post(self, request, **kwargs):
        submission = request.data
        # TODO: What to do when it's not found?
        try:
            task_interaction_model = TaskInteraction.objects \
                .get(pk=int(kwargs['pk']))
        except TaskInteraction.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            # if we fail validation or anything else all is well and nothing
            # is committed
            with transaction.atomic():
                self.save_data_to_mapped_models(submission['auditors'],
                                                NAME_TO_AUDITOR,
                                                task_interaction_model)
                self.save_data_to_mapped_models(submission['steps'],
                                                NAME_TO_STEP,
                                                task_interaction_model)
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class TaskView(View):
    def get(self, request, **kwargs):
        try:
            task = Task.objects.get(pk=kwargs['pk'])
        except Task.DoesNotExist:
            raise Http404(_('No such task'))
        if task.number_simultaneous_users > 1:
            # TODO: Support for lobby
            raise Exception('Support for simultaneous users '
                            'has not yet been coded')
        if task.task_dependencies.count() > 0:
            # TODO: Support for checking if user has completed previous tasks
            raise Exception('Support for interdependent tasks '
                            'has not yet been coded')

        # TODO: Find a way to cut down on the number of queries these two for loops will have to make
        auditors = []
        for auditor_model_name in NAME_TO_AUDITOR.values():
            auditor_model = apps.get_model('survey', auditor_model_name)
            auditors.extend(auditor_model.objects.filter(task=task))

        steps = []
        for step_model_name in NAME_TO_STEP.values():
            step_model = apps.get_model('survey', step_model_name)
            steps.extend(step_model.objects.filter(task=task))
        steps.sort(key=lambda x: x.step_num)

        auditor_script_locations = [auditor.script_location for auditor in
                                    auditors]

        # serves to only get one instance of each script
        # needed for steps, since it is valid
        # for a user to have multiple steps (e.g. multiple choice)
        step_script_locations = list(
            set([step.script_location for step in steps]))

        task_interaction_model = TaskInteraction.objects.create(task=task)

        return TemplateResponse(
            request, task.survey_wrap_template,
            status=status.HTTP_200_OK,
            context={'auditors': auditors,
                     'steps': steps,
                     'task': task,
                     'task_interaction_model': task_interaction_model,
                     'auditor_script_locations': auditor_script_locations,
                     'step_script_locations': step_script_locations})


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

    def _render_auditors_meta_xml(self, request, task):
        # get instances in a dict of the auditors that are actually
        # attached to our task
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

    def _render_task_meta_xml(self, request, task):
        auditors_xml = self._render_auditors_meta_xml(request, task)
        steps_xml = self._render_steps_meta_xml(request, task)
        renderer = XMLBodyRenderer(root_tag_name='task_meta')
        task_xml = renderer.render(task.serialize_info_to_dict())
        return ''.join([task_xml, auditors_xml, steps_xml])

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
                                         'data': step.serialize_data()})
            steps_serialized[step_name] = serialized_steps
        return steps_serialized

    def _render_task_interactions(self, request, task_interactions):
        if task_interactions.count() == 0:
            return ''

        auditors = self._get_related_auditors(task_interactions[0].task)
        steps = self._get_related_steps(task_interactions[0].task)

        step_related_names = []
        for step_list in steps.values():
            step_related_names.append(
                '%s_set' % step_list[0].data_model._meta.default_related_name
            )
        auditor_related_names = [
            '%s_set' % auditor.data_model._meta.default_related_name for
            auditor in auditors.values()
            ]
        # TODO: Test that this is preventing queries in the for loop below
        task_interactions = task_interactions \
            .prefetch_related(auditor_related_names) \
            .prefetch_related(step_related_names)

        renderer = XMLBodyRenderer(root_tag_name='interaction')
        interactions = []
        for interaction in task_interactions:
            interaction = {'meta': interaction.serialize_info_to_dict()}
            interaction['auditors'] = self._get_auditors_dict(interaction,
                                                              auditors)
            interaction['steps'] = self._get_steps_dict(interaction,
                                                        steps)
            interactions.append(renderer.render(interaction))
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

    def get(self, request, primary_keys):
        primary_keys = [int(n) for n in primary_keys.split(',')]
        # "trust but verify"
        tasks = Task.objects.filter(pk__in=primary_keys)
        if tasks.count() != len(primary_keys):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        response_iterator = self._get_response_iterator(request, tasks)
        return StreamingHttpResponse(response_iterator,
                                     content_type='text/xml')
