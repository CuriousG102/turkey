from django.apps import apps
from django.db import transaction
from django.template.response import TemplateResponse
from django.views.generic import View
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from .auditors import NAME_TO_AUDITOR
from .steps import NAME_TO_STEP
from .models import Task, TaskInteraction


# TODO: Authentication
class RecordSubmission(APIView):
    def save_data_to_mapped_models(self, data, map,
                                   task_interaction_model):
        associated_models = []
        task = task_interaction_model.task
        # model fetch step
        for name, model_data in data.items():
            associated_models.append(apps.get_model('survey', map[name])
                                     .objects.filter(task=task))

        # save step
        for name, model_data, associated_models in zip(data.items(),
                                                       associated_models):
            for model in associated_models:
                model.handle_submission_data(model_data,
                                             task_interaction_model)

    def post(self, request, **kwargs):
        submission = request.data
        # TODO: What to do when it's not found?
        try:
            task_interaction_model = TaskInteraction.objects \
                .get(pk=kwargs['pk'])
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


class TaskView(View):
    def get(self, request, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
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

        task_interaction_model = TaskInteraction(task=task)
        task_interaction_model.save()

        return TemplateResponse(
            request, task.survey_wrap_template,
            status=status.HTTP_200_OK,
            context={'auditors': auditors,
                     'steps': steps,
                     'task': task,
                     'task_interaction_model': task_interaction_model,
                     'auditor_script_locations': auditor_script_locations,
                     'step_script_locations': step_script_locations})
