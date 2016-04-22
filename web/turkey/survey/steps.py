from django.core.exceptions import ValidationError
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# register and build your step models here
from .models import Step, StepData, Model

NAME_TO_STEP = {
    'multiple_choice': 'StepMultipleChoice',
    'text_input': 'StepTextInput',
    'multiple_answers': 'StepMultipleAnswers'
}


class StepMultipleChoiceData(StepData):
    general_model = models.ForeignKey('StepMultipleChoice')
    response = models.ForeignKey('StepMultipleChoiceResponse')

    def clean(self):
        # TODO: Write a test for this
        if self.response not in \
                self.general_model.stepmultiplechoiceresponse_set.all():
            raise ValidationError(
                _('Response that is not in the set of responses'))
        super().clean()

    class Meta(StepData.Meta):
        abstract = False


class StepMultipleChoice(Step):
    inlines = ['StepMultipleChoiceResponse']
    script_location = 'survey/js/steps/multiple_choice.js'
    template_file = 'survey/steps/multiple_choice.html'
    data_model = StepMultipleChoiceData
    title = models.CharField(
        max_length=144,
        verbose_name=_('Title'),
        help_text=_(
            'Title for multiple choice prompt. Choose carefully. '
            'This and associated '
            'responses are not allowed to change after the first '
            'user has responded to this multiple choice step. Then, '
            'you must create a new Multiple Choice Step'
        )
    )
    text = models.TextField(
        verbose_name=_('Multiple Choice Text'),
        help_text=_(
            'The text to go along with your multiple '
            'choice prompt. Choose carefully. This and associated '
            'responses are not allowed to change after the first '
            'user has responded to this multiple choice step. Then, '
            'you must create a new Multiple Choice Step'
        )
    )
    randomize_order = models.BooleanField(
        verbose_name=_('Randomize Response Order'),
        help_text=_('Randomizes the order in which responses are presented '
                    'to the user under a Multiple Choice Step if selected'),
        default=False
    )

    def serialize_info_to_dict(self):
        serialized_info = super().serialize_info_to_dict()
        responses = []
        for response in self.stepmultiplechoiceresponse_set.all():
            responses.append(response.serialize_info_to_dict())
        serialized_info['responses'] = responses
        return serialized_info

    def get_template_code(self, additional_context=None):
        if additional_context is None:
            additional_context = dict()
        responses = self.stepmultiplechoiceresponse_set.all()
        if self.randomize_order:
            responses = responses.order_by('?')
        additional_context.update({'responses': responses})
        return super().get_template_code(additional_context)

    class Meta(Step.Meta):
        verbose_name = _('Multiple Choice Step')
        abstract = False


class StepMultipleChoiceResponse(Model):
    multiple_choice_model = models.ForeignKey(
        'StepMultipleChoice',
        verbose_name=_('Associated Multiple Choice Step for Response')
    )
    text = models.TextField(
        verbose_name=_('Multiple Choice Response Text'),
        help_text=_('Text for one of the responses to a Multiple Choice Step')
    )
    order = models.IntegerField(
        verbose_name=_('Response Number'),
        help_text=_(
            'Controls the order that responses linked to a '
            'Multiple Choice Step are to be rendered. The field can be left '
            'blank but this only really makes sense if you randomize order of '
            'responses in the Multiple Choice Step'),
        null=True,
        blank=True
    )

    def clean(self):
        # trip a validation error if there are already responses
        self.multiple_choice_model.clean()
        super().clean()

    class Meta(Step.Meta):
        verbose_name = _('Multiple Choice Step Response')
        abstract = False
        ordering = ['order']


class StepTextInputData(StepData):
    general_model = models.ForeignKey('StepTextInput')
    response = models.TextField(verbose_name=_('StepTextInputResponse'),
                                help_text=_('User\'s text response'))

    class Meta(StepData.Meta):
        abstract = False

class StepTextInput(Step):
    script_location = 'survey/js/steps/text_input.js'
    template_file = 'survey/steps/text_input.html'
    data_model = StepTextInputData
    title = models.CharField(
        max_length=144,
        verbose_name=_('Title'),
        help_text=_(
            'Title for text input prompt. Choose carefully. '
            'This and associated '
            'responses are not allowed to change after the first '
            'user has responded to this text input step. Then, '
            'you must create a new Text Input Step'
        )
    )
    text = models.TextField(
        verbose_name=_('Text Input Text'),
        help_text=_(
            'The text to go along with your text '
            'input prompt. Choose carefully. This and associated '
            'responses are not allowed to change after the first '
            'user has responded to this text input step. Then, '
            'you must create a new Text Input Step'
        )
    )
    randomize_order = models.BooleanField(
        verbose_name=_('TODO!!!!!!!!!!!!'),
        help_text=_('TODO: This is not needed for this step but it is required '
                    'by the db.....'),
        default=False
    )

    class Meta(Step.Meta):
        verbose_name = _('Text Input Step')
        abstract = False


class StepMultipleAnswersData(StepData):
    general_model = models.ForeignKey('StepMultipleAnswers')
    response = models.ForeignKey('StepMultipleAnswersResponse')

    def clean(self):
        # TODO: Write a test for this
        if self.response not in \
                self.general_model.stepmultipleanswersresponse_set.all():
            raise ValidationError(
                _('Response that is not in the set of responses'))
        super().clean()

    class Meta(StepData.Meta):
        abstract = False


class StepMultipleAnswers(Step):
    inlines = ['StepMultipleAnswersResponse']
    script_location = 'survey/js/steps/multiple_answers.js'
    template_file = 'survey/steps/multiple_answers.html'
    data_model = StepMultipleAnswersData
    title = models.CharField(
        max_length=144,
        verbose_name=_('Title'),
        help_text=_(
            'Title for multiple answers prompt. Choose carefully. '
            'This and associated '
            'responses are not allowed to change after the first '
            'user has responded to this multiple answers step. Then, '
            'you must create a new Multiple Answers Step'
        )
    )
    text = models.TextField(
        verbose_name=_('Multiple Answers Text'),
        help_text=_(
            'The text to go along with your text '
            'input prompt. Choose carefully. This and associated '
            'responses are not allowed to change after the first '
            'user has responded to this multiple answers step. Then, '
            'you must create a new Multiple Answers Step'
        )
    )
    randomize_order = models.BooleanField(
        verbose_name=_('Randomize Response Order'),
        help_text=_('Randomizes the order in which responses are presented '
                    'to the user under a Multiple Answers Step if selected'),
        default=False
    )

    def serialize_info_to_dict(self):
        serialized_info = super().serialize_info_to_dict()
        responses = []
        for response in self.stepmultipleanswersresponse_set.all():
            responses.append(response.serialize_info_to_dict())
        serialized_info['responses'] = responses
        return serialized_info

    def get_template_code(self, additional_context=None):
        if additional_context is None:
            additional_context = dict()
        responses = self.stepmultipleanswersresponse_set.all()
        if self.randomize_order:
            responses = responses.order_by('?')
        additional_context.update({'responses': responses})
        return super().get_template_code(additional_context)

    class Meta(Step.Meta):
        verbose_name = _('Multiple Answers Step')
        abstract = False


class StepMultipleAnswersResponse(Model):
    multiple_answers_model = models.ForeignKey(
        'StepMultipleAnswers',
        verbose_name=_('Associated Multiple Answers Step for Response')
    )
    text = models.TextField(
        verbose_name=_('Multiple Answers Response Text'),
        help_text=_('Text for one of the responses to a Multiple Answers Step')
    )
    order = models.IntegerField(
        verbose_name=_('Response Number'),
        help_text=_(
            'Controls the order that responses linked to a '
            'Multiple Answers Step are to be rendered. The field can be left '
            'blank but this only really makes sense if you randomize order of '
            'responses in the Multiple Answers Step'),
        null=True,
        blank=True
    )

    def clean(self):
        # trip a validation error if there are already responses
        self.multiple_answers_model.clean()
        super().clean()

    class Meta(Step.Meta):
        verbose_name = _('Multiple Answers Step Response')
        abstract = False
        ordering = ['order']
