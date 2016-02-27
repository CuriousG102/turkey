from django.db import models
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from .steps import *  # we have to get all the user defined models from steps
from .auditors import *  # we have to get all the user defined models from auditors


class Model(models.Model):
    """
    Abstract model to be used to define all our top-level models. Holds fields
    that we desire all models to have, like time created and time updated.
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        abstract = True


def not_less_than_one(value):
    if value < 1:
        raise ValidationError(
            _('If number_simultaneous_users is < 1, the value makes no sense.')
        )


# Create your models here.
class Task(Model):
    number_simultaneous_users = models.IntegerField(
        verbose_name=_('Number of simultaneous users'),
        help_text=_('Number of users who need to be in the lobby and ready '
                    'to begin before they may start the task'),
        validators=not_less_than_one
    )
    task_dependencies = models.ManyToManyField(
        'Task',
        verbose_name=_('Task Dependencies'),
        help_text=_('Tasks that must be completed before this task by a given user')
    )
    survey_wrap_template = 'survey/survey_default_template.html'
    lobby_template = 'survey/lobby_default_template.html'
    owners = models.ManyToManyField(
        User,
        verbose_name=_('Owners'),
        help_text=_('Users with permission to view and modify')
    )

    class Meta:
        verbose_name = _('Interactive Task')
        ordering = ['-updated', '-created']


class DataModel(Model):
    """
    Exists to link specific instances of data to a general instance of auditor
    and step that is linked to HIT. So for example, there is a general auditor/step
    with configuration created by the user, and then when there is a submission on a
    task, that auditor/step creates an instance of its data model with the captured
    data from the user, and that data model points back at the auditor/step
    """

    class Meta:
        abstract = True
        ordering = ['-updated', '-created']


class StepDataModel(DataModel):
    general_model = models.ForeignKey('Step')


class AuditorDataModel(DataModel):
    general_model = models.ForeignKey('Auditor')


class TaskLinkedModel:
    task = models.ForeignKey(
        'Task',
        verbose_name=_('Associated Task'),
        help_text=_('Task that this is linked to')
    )


class EventAndSubmission:
    template_code = 'survey/my_step_template.html'
    data_model = DataModel

    def handle_submission_data(self, data):
        """
        Parameter data will be created directly from the JSON sent via
        auditor or step code for submission. How you handle it here is up
        to you. You can create a dictionary or list of dictionaries for
        filling the data model linked your Step or Auditor via data_model.
        As long as the keys and corresponding Python primitives (values)
        match your data model you can pass that dictionary or list of
        dictionaries to save_processed_data_to_model and it will create
        those data models for you. Alternatively, you can choose to handle
        the model creation on your own. This will be necessary if your data
        model has relations with models other than the your Step or Auditor
        model. The base case of this method is written for the simplest
        possible scenario: The data coming in from the submission is a dictionary,
        it directly matches your data model, and so it can be passed directly to
        save_processed_data_to_model without validation or translation.
        """
        self.save_processed_data_to_model(data)

    def get_template_code(self):
        return render_to_string(self.template_code)

    def save_processed_data_to_model(self, processed_data):
        assert (type(processed_data) == list or type(processed_data) == dict)
        if type(processed_data) != list:
            processed_data = [processed_data]
        for dictionary in processed_data:
            model_instance = self.data_model()
            for key, value in dictionary.items():
                setattr(model_instance, key, value)
            model_instance.general_model = self
            model_instance.save()


class Step(models.Model, EventAndSubmission, TaskLinkedModel):
    step_num = models.IntegerField(
        verbose_name=_('Step Number'),
        help_text=_('Controls the order that steps linked to a task are to be '
                    'taken in by the user')
    )

    class Meta:
        abstract = True
        verbose_name = _('Step')
        verbose_name_plural = _('Steps')
        ordering = ['task', 'step_num', '-updated', '-created']


class Auditor(models.Model, EventAndSubmission, TaskLinkedModel):
    class Meta:
        abstract = True
        verbose_name = _('Auditor')
        verbose_name_plural = _('Auditors')
        ordering = ['task', '-updated', '-created']
