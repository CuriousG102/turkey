from django.contrib import admin
from django.apps import apps
from django.core.urlresolvers import reverse
from .models import Task
from .steps import NAME_TO_STEP
from .auditors import NAME_TO_AUDITOR


def create_step_or_auditor_admin(model):
    class StepAuditorAdmin(admin.ModelAdmin):
        def get_model_perms(self, request):
            # hacky way to keep this
            # from showing up in the list of models
            return {}

    admin.site.register(model, StepAuditorAdmin)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    def get_models_change_pages(self, models):
        links = []
        for model in models:
            links.append(reverse('admin:%s_%s_change' % (model._meta.app_label,
                                                         model._meta.model_name),
                                 args=(model.pk,)))
        return links

    def get_related_models_from_mapping(self, task, mapping):
        related_models = []
        for model_name in mapping.values():
            model = apps.get_model('survey', model_name)
            related_models.extend(model.objects.filter(task=task))
        return related_models

    def render_change_form(self, request, context, **kwargs):
        task = kwargs['obj']
        related_step_models = sorted(
            self.get_related_models_from_mapping(task, NAME_TO_STEP),
            key=lambda step: step.step_num
        )
        related_steps = zip(
            self.get_models_change_pages(related_step_models),
            related_step_models
        )
        related_auditor_models = self \
            .get_related_models_from_mapping(task, NAME_TO_AUDITOR)
        related_auditors = zip(
            self.get_models_change_pages(related_auditor_models),
            related_auditor_models
        )
        context.update({
            'related_steps': related_steps,
            'related_auditors': related_auditors
        })
        return super().render_change_form(request, context, **kwargs)
