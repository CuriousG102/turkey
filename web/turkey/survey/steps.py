from django.core.exceptions import ValidationError
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# register and build your step models here
from .models import Step, StepData, Model

NAME_TO_STEP = {
    'multiple_choice': 'StepMultipleChoice'
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
        help_text=_(
            'Text for one of the responses to a Multiple Choice Step'
        )
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

# class StepTextResponseData(StepData):
#     general_model = models.ForeignKey('StepTextResponse')
#     response = models.TextField(verbose_name=_('Response'),
#                                 help_text=_('User\'s text response'))
#     text = models.TextField(
#         verbose_name=_('Text Response Prompt'),
#         help_text=_(
#             'The text to go along with your response '
#             'choice prompt. Choose carefully. This and associated '
#             'responses are not allowed to change after the first '
#             'user has responded to this multiple choice step. Then, '
#             'you must create a new Multiple'
#         )
#     )
#
#     class Meta(StepData.Meta):
#         abstract = False
#
#
# class StepTextResponse(Step):
#     data_model = StepTextResponseData
#     prompt = models.TextField(verbose_name=_('Prompt'))
#
#     class Meta(Step.Meta):
#         abstract = False
