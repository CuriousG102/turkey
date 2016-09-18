from django.core import serializers
from django.db import models
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Model(models.Model):
    """
    Abstract model to be used to define all our top-level models. Holds fields
    that we desire all models to have, like time created and time updated.
    """
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_('Created At'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def serialize_info_to_dict(self):
        return serializers.serialize('python', [self])[0]

    def __str__(self):
        return self.updated.strftime(str(_('Updated: %B %d, %Y')))

    class Meta:
        abstract = True


# Create your models here.
class Task(Model):
    survey_wrap_template = 'survey/survey_default_template.html'
    lobby_template = 'survey/lobby_default_template.html'
    # TODO: Actually enforce this
    owners = models.ManyToManyField(
        User,
        verbose_name=_('Owners'),
        help_text=_('Users with permission to view and modify')
    )
    survey_name = models.CharField(max_length=144,
                                   verbose_name=_('Survey Name'),
                                   help_text=_(
                                       'This is exposed to the user: Name of '
                                       'the survey they\'re taking. It is an '
                                       'optional field, as it is not relevant '
                                       'if this is an external task.'),
                                   blank=True,
                                   null=True
                                   )

    external = models.BooleanField(default=False,
                                   verbose_name=_('External Hit'),
                                   help_text=_(
                                       'If the task is not external, we will host it '
                                       'and you can design it on our platform. If it is '
                                       'external, you should mark this true, and we will '
                                       'provide you with embed code to use on your HIT '
                                       'with your selected auditors.')
                                   )

    def __str__(self):
        return ' '.join(['%s: ' % self._meta.verbose_name, self.survey_name,
                         super().__str__()])

    def clean(self):
        if self.pk and self.taskinteraction_set.all().exists():
            original = type(self).objects.get(pk=self.pk)
            if self.survey_name != original.survey_name:
                raise ValidationError(_('Can\'t change the name of the '
                                         'HIT as there are already '
                                         'responses'))
            if self.external != original.external:
                raise ValidationError(_('Can\'t change whether the HIT is '
                                         'internal or external because there '
                                         'is already collected data'))

        if not self.external and not self.survey_name:
            raise ValidationError(_('%s cannot be blank because this is not '
                                     'an external HIT') %
                                   self._meta.get_field('survey_name').verbose_name)

    class Meta:
        verbose_name = _('Interactive Task')
        ordering = ['-updated', '-created']


class _DataModel(Model):
    """
    Exists to link specific instances of data to a general instance of auditor
    and step that is linked to HIT. So for example, there is a general auditor/step
    with configuration created by the user, and then when there is a submission on a
    task, that auditor/step creates an instance of its data model with the captured
    data from the user, and that data model points back at the auditor/step
    """
    task_interaction_model = models.ForeignKey('TaskInteraction')

    @classmethod
    def has_instances_for_task_interaction(cls, task_interaction):
        return cls.objects.filter(task_interaction_model=task_interaction).exists()

    def __str__(self):
        return ' '.join(
            [self._meta.verbose_name or
             _('%s object,') % self.__class__.__name__,
             super().__str__()])

    class Meta:
        abstract = True
        ordering = ['-updated', '-created']


class StepData(_DataModel):
    pass
    #  general_model = models.ForeignKey('Step') <-- field you must implement


class AuditorData(_DataModel):
    pass
    #  general_model = models.ForeignKey('Auditor') <--
    #                                                  field you must implement


# TODO: Should inherit from Model, but this causes field clashes, necessitating inheriting Model as well in some classes. Bad stuff.
class _TaskLinkedModel(Model):
    task = models.ForeignKey(
        'Task',
        verbose_name=_('Associated Task'),
        help_text=_('Task that this is linked to')
    )

    def __str__(self):
        return ' '.join(
            [str(self._meta.verbose_name) or
             _('%s object,') % self.__class__.__name__,
             _('Linked Task: [%s]') % self.task,
             str(super().__str__())])

    class Meta:
        abstract = True


class TaskInteraction(_TaskLinkedModel):
    """
    Created for each new HIT with Task. Data models for Steps and Auditors
    tie back to this.

    The obvious: We need to know who each auditor and step data entry is
    associated with.

    The other consideration: We can see what percentage of people are
    completing our HITs by calculating (task interactions with linked submitted steps)/(task interactions)
    """

    class Meta:
        verbose_name = _('Task Interaction')


class _EventAndSubmissionModel(_TaskLinkedModel):
    script_location = 'survey/js/step_or_auditor/my_example.js'
    data_model = _DataModel
    has_custom_admin = False
    # shortcut to allow users to have related models that need
    # to be edited for their step or auditor and still
    # autogenerate admin page
    inlines = []

    def has_data_for_task_interaction(self, task_interaction):
        return self.data_model.has_instances_for_task_interaction(task_interaction)

    @staticmethod
    def processed_data_to_list(processed_data):
        if not (type(processed_data == list or type(processed_data == dict))):
            raise ValidationError(_('processed_data is not list or dict'))
        if type(processed_data) != list:
            processed_data = [processed_data]
        return processed_data

    def save_processed_data_to_model(self, processed_data,
                                     task_interaction):
        """
        Simple helper function. Takes a list of dictionaries or a single
        dictionary in the parameter processed_data, where the keys
        are names of fields on the class's data_model and the values
        are values to be saved on those fields. Not appropriate for all
        situations but fits many, especially with auditors.
        """

        processed_data = self.processed_data_to_list(processed_data)
        for dictionary in processed_data:
            model_instance = self.data_model()
            for key, value in dictionary.items():
                try:
                    field = type(self).data_model._meta.get_field(key)
                except FieldDoesNotExist:
                    raise ValidationError(
                        _('processed_data contains dictionaries '
                          'without matching fields'))
                if type(field) is models.ForeignKey:
                    try:
                        value = field.related_model.objects.get(pk=value)
                    except field.related_model.DoesNotExist:
                        raise ValidationError(_('Related Field Not Found'))
                setattr(model_instance, key, value)
            model_instance.general_model = self
            model_instance.task_interaction_model = task_interaction
            model_instance.full_clean()
            model_instance.save()

    def handle_submission_data(self, data, task_interaction):
        raise NotImplementedError()

    def serialize_data(self, task_interaction):
        # TODO: Implement prefetching
        return [datum.serialize_info_to_dict() for datum in
                self.data_model.objects.filter(
                    task_interaction_model=task_interaction)]

    def __str__(self):
        return _('%s for: [%s] %s') % \
               (self._meta.verbose_name or
                '%s object' % self.__class__.__name__,
                self.task,
                self.updated.strftime(str(_('Updated: %B %d, %Y'))))

    def clean(self):
        # if step/auditor object's task already has user data
        # we can't let them alter it or auditors/steps
        if self.task.taskinteraction_set.count() > 0:
            raise ValidationError(
                _('Steps and Auditors for %s may not be changed '
                  'or added because it already has '
                  'user interactions and data gathered would '
                  'be invalidated') % self.task
            )
        super().clean()

    class Meta:
        abstract = True


class Step(_EventAndSubmissionModel):
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

    def handle_submission_data(self, data, task_interaction):
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
        model has relations that are not represented by a single foreign key.
        The base case of this method is written for the simplest
        possible scenario: The data coming in from the submission is a
        dictionary whose keys are ids for instances of your model. The
        values of those keys is a list of dictionaries or a dictionary,
        whose keys and values
        directly match your data model, and so can be passed directly to
        save_processed_data_to_model without validation or translation.
        """
        self.save_processed_data_to_model(data[str(self.pk)],
                                          task_interaction)

    def get_template_code(self, additional_context=None):
        if additional_context is None:
            additional_context = dict()
        context = {'step_instance': self}
        context.update(additional_context)
        return render_to_string(self.template_file,
                                context)

    @property
    def template_code(self):
        # get_template_code is not inlined so the user can override that
        # call without having to understand how @property or the template
        # system works in its entirety
        return self.get_template_code()

    def clean(self):
        if self.task.external:
            raise ValidationError(_('Can\'t create step for external HIT'))
        super().clean()

    class Meta:
        abstract = True
        verbose_name = _('Step')
        verbose_name_plural = _('Steps')
        ordering = ['task', 'step_num', '-updated', '-created']


class Auditor(_EventAndSubmissionModel):
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
        super().clean()

    def handle_submission_data(self, data, task_interaction):
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
        model has relations that are not represented by a single foreign key.
        The base case of this method is written for the simplest
        possible scenario: The data coming in from the submission is a
        list of dictionaries or a single dictionary
        whose keys and values directly
        match your data model, and so can be passed directly to
        save_processed_data_to_model without validation or translation.
        """
        self.save_processed_data_to_model(data, task_interaction)

    class Meta:
        abstract = True
        verbose_name = _('Auditor')
        verbose_name_plural = _('Auditors')
        ordering = ['task', '-updated', '-created']


from .steps import *  # we have to get all the user defined models from steps
from .auditors import *  # we have to get all the user defined models from
