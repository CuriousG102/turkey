from django.apps import apps
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
            model = apps.get_model('survey', map[name])
            # user defined handle_submission data simply needs to return a flat
            # map in the form of a Python dictionary between field names and values
            processed_data_dictionary = model.handle_submission_data(model_data)
            model_instance = model()
            for key, value in processed_data_dictionary.items():
                setattr(model_instance, key, value)
            model_instance.task = task
            model_instance.save()

    def post(self, request, **kwargs):
        submission = request.data
        task = Task.objects.get(pk=kwargs['pk'])
        self.save_data_to_mapped_models(submission.auditors, NAME_TO_AUDITOR, task)
        self.save_data_to_mapped_models(submission.steps, NAME_TO_STEP, task)
        return Response(status=status.HTTP_201_CREATED)
