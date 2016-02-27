from django.apps import apps
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
            model = apps.get_model('survey', map[name]).get(task=task)
            model.handle_submission_data(model_data)

    def post(self, request, **kwargs):
        submission = request.data
        task = Task.objects.get(pk=kwargs['pk'])
        self.save_data_to_mapped_models(submission.auditors, NAME_TO_AUDITOR, task)
        self.save_data_to_mapped_models(submission.steps, NAME_TO_STEP, task)
        return Response(status=status.HTTP_201_CREATED)

class TaskView(View):
    def get(self, request):
        pass
