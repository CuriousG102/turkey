from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SurveyConfig(AppConfig):
    name = 'survey'
    verbose_name = _('Survey')