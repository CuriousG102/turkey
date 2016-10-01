from django.conf import settings

SURVEY_CONFIG = {
    'TOKEN_NAME': 'turkey_token'
}

USER_SETTINGS = getattr(settings, 'SURVEY_CONFIG', None)

if USER_SETTINGS:
    for key, value in USER_SETTINGS.items():
        SURVEY_CONFIG[key] = value
