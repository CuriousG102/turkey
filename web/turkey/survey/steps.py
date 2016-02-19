# register and build your step models here
from django.db import models
from .models import Step

URL_NAME_TO_STEP = {
    'multiple_choice_text': 'StepMultipleChoiceText',
    'multiple_choice_media': '',
    'choose_category': '',
    'text_input': '',
}

class StepMultipleChoiceText(Step):
    def take_submission_json(self, json):
        pass

    def get_template_code(self):
        return render_to_string('survey/multiple_choice_text_template.html')

    def handle_incoming_json(self, json):
        pass
        # do the json stuff

    class Meta(Step.Meta):
        abstract = False

    def __str__(self):
        self.get_template_code()
