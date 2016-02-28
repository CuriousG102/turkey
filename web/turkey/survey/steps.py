# register and build your step models here
from .models import Step

NAME_TO_STEP = {
    'multiple_choice_text': 'StepMultipleChoiceText',
    'multiple_choice_media': '',
    'choose_category': '',
    'text_input': '',
}

class StepMultipleChoiceText(Step):
    class Meta(Step.Meta):
        abstract = False
