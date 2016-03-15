from django.contrib import admin
from django.apps import apps
from .models import Task
from .steps import NAME_TO_STEP
from .auditors import NAME_TO_AUDITOR


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    def get_related_models_from_mapping(self, task, mapping):
        related_models = []
        for model_name in mapping.values():
            model = apps.get_model('survey', model_name)
            related_models.extend(model.objects.filter(task=task))
        return related_models

    def render_change_form(self, request, context, **kwargs):
        task = kwargs['obj']
        related_steps = self\
            .get_related_models_from_mapping(task, NAME_TO_STEP)
        related_auditors = self\
            .get_related_models_from_mapping(task, NAME_TO_AUDITOR)
        context.update({
            'related_steps': related_steps,
            'related_auditors': related_auditors
        })
        return super().render_change_form(request, context, **kwargs)