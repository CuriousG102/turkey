from django.db import models
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from .steps import *  # we have to get all the user defined models from steps
from .auditors import *  # we have to get all the user defined models from


# auditors


class Model(models.Model):
    """
    Abstract model to be used to define all our top-level models. Holds fields
    that we desire all models to have, like time created and time updated.
    """
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_('Created At'))
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
        help_text=_(
            'Tasks that must be completed before this task by a given user')
    )
    survey_wrap_template = 'survey/survey_default_template.html'
    lobby_template = 'survey/lobby_default_template.html'
    owners = models.ManyToManyField(
        User,
        verbose_name=_('Owners'),
        help_text=_('Users with permission to view and modify')
    )
    survey_name = models.CharField(max_length=144,
                                   verbose_name=_('Survey Name'),
                                   help_text=(
                                       'This is exposed to the user: Name of '
                                       'the survey they\'re taking'))

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


class StepData(DataModel):
    general_model = models.ForeignKey('Step')


class AuditorData(DataModel):
    general_model = models.ForeignKey('Auditor')


class TaskLinkedModel(models.Model):
    task = models.ForeignKey(
        'Task',
        verbose_name=_('Associated Task'),
        help_text=_('Task that this is linked to')
    )


class EventAndSubmissionModel(Model):
    script_location = 'survey/step_or_auditor/my_example.js'
    data_model = DataModel

    def save_processed_data_to_model(self, processed_data):
        """
        Simple helper function. Takes a list of dictionaries or a single
        dictionary in the parameter processed_data, where the keys
        are names of fields on the class's data_model and the values
        are values to be saved on those fields. Not appropriate for all
        situations but fits many, especially with auditors.
        """
        assert (type(processed_data) == list or type(processed_data) == dict)
        if type(processed_data) != list:
            processed_data = [processed_data]
        for dictionary in processed_data:
            model_instance = self.data_model()
            for key, value in dictionary.items():
                setattr(model_instance, key, value)
            model_instance.general_model = self
            model_instance.save()


class Step(EventAndSubmissionModel, TaskLinkedModel):
    """
    Your step should include some way to distinguish it from another instance of
    the same class in its template code, because the user may make multiple
    instances of the same step model (e.g. two multiple choice questions).
    That way, the associated script can pick up on those different instances,
    for example by seeing that they have different numbers associated with
    their primary keys in the id attribute on one of their tags
    """
    template_file = 'survey/my_step_template.html'
    step_num = models.IntegerField(
        verbose_name=_('Step Number'),
        help_text=_('Controls the order that steps linked to a task are to be '
                    'taken in by the user')
    )

    def handle_submission_data(self, data):
        """
        Parameter data will be created directly from the JSON sent via
        step code for submission. How you handle it here is up
        to you. You can create a dictionary or list of dictionaries for
        filling the data model linked your Step via data_model.
        As long as the keys and corresponding Python primitives (values)
        match your data model you can pass that dictionary or list of
        dictionaries to save_processed_data_to_model and it will create
        those data models for you. Alternatively, you can choose to handle
        the model creation on your own. This will be necessary if your data
        model has relations with models other than the your Step or Auditor
        model. The base case of this method is written for the simplest
        possible scenario: The data coming in from the submission is a
        dictionary whose keys are ids for instances of your model. The
        values of those keys are also dictionaries, whose keys and values
        directly matches your data model, and so can be passed directly to
        save_processed_data_to_model without validation or translation.
        """
        self.save_processed_data_to_model(data[str(self.pk)])

    def get_template_code(self):
        return render_to_string(self.template_file,
                                {'step_instance': self})

    @property
    def template_code(self):
        # get_template_code is not inlined so the user can override that
        # call without having to understand how @property or the template
        # system works in its entirety
        return self.get_template_code()

    class Meta:
        abstract = True
        verbose_name = _('Step')
        verbose_name_plural = _('Steps')
        ordering = ['task', 'step_num', '-updated', '-created']


class Auditor(EventAndSubmissionModel, TaskLinkedModel):
    # https://docs.djangoproject.com/en/1.9/ref/models/instances/#validating-objects
    def clean(self):
        # it is not valid to create two auditors for the same task
        try:
            type(self).objects.get(task=self.task)
            # if we got here there's an instance of the auditor that
            # already exists for this task
            raise ValidationError(_('There may only be one instance of the'
                                    'same auditor for each task'))
        except type(self).DoesNotExist:
            pass  # this is what we want

    def handle_submission_data(self, data):
        """
        Parameter data will be created directly from the JSON sent via
        auditor code for submission. How you handle it here is up
        to you. You can create a dictionary or list of dictionaries for
        filling the data model linked your Auditor via data_model.
        As long as the keys and corresponding Python primitives (values)
        match your data model you can pass that dictionary or list of
        dictionaries to save_processed_data_to_model and it will create
        those data models for you. Alternatively, you can choose to handle
        the model creation on your own. This will be necessary if your data
        model has relations with models other than the your Step or Auditor
        model. The base case of this method is written for the simplest
        possible scenario: The data coming in from the submission is a
        dictionary, whose keys and values directly match your data model,
        and so can be passed directly to save_processed_data_to_model without
        validation or translation.
        """
        self.save_processed_data_to_model(data)

    class Meta:
        abstract = True
        verbose_name = _('Auditor')
        verbose_name_plural = _('Auditors')
        ordering = ['task', '-updated', '-created']
