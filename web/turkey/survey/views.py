from django.apps import apps
from django.template.response import TemplateResponse
from django.views.generic import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .auditors import NAME_TO_AUDITOR
from .steps import NAME_TO_STEP
from .models import Task


# TODO: Authentication
# TODO: Content type restrictions
class RecordSubmission(APIView):
    def save_data_to_mapped_models(self, data, map, task):
        for name, model_data in data.items():
            models = apps.get_model('survey', map[name]).objects.filter(task=task)
            for model in models:
                model.handle_submission_data(model_data)

    def post(self, request, **kwargs):
        submission = request.data
        task = Task.objects.get(pk=kwargs['pk'])
        self.save_data_to_mapped_models(submission['auditors'], NAME_TO_AUDITOR, task)
        self.save_data_to_mapped_models(submission['steps'], NAME_TO_STEP, task)
        return Response(status=status.HTTP_201_CREATED)


class TaskView(View):
    def get(self, request, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
        if task.number_simultaneous_users > 1:
            # TODO: Support for lobby
            raise Exception('Support for simultaneous users has not yet been coded')
        if task.task_dependencies.count() > 0:
            # TODO: Support for checking if user has completed previous tasks
            raise Exception('Support for interdependent tasks has not yet been coded')

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

        return TemplateResponse(request, task.survey_wrap_template, status=status.HTTP_200_OK,
                                context={'auditors': auditors,
                                         'steps': steps,
                                         'task': task})
