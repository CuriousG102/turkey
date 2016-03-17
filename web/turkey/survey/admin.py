from django.conf.urls import url
from django.contrib import admin
from django.apps import apps
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
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


def create_step_or_auditor_admins(model_name_list):
    for model_name in model_name_list:
        create_step_or_auditor_admin(apps.get_model('survey', model_name))


create_step_or_auditor_admins(NAME_TO_STEP.values())
create_step_or_auditor_admins(NAME_TO_AUDITOR.values())


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    step_add_template = 'survey/admin/step_add_template.html'
    auditor_add_template = 'survey/admin/auditor_add_template.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^\d+/add_step/$',
                self.admin_site.admin_view(self.add_step_view,
                                           cacheable=True)),
            url(r'^\d+/add_auditor/$',
                self.admin_site.admin_view(self.add_auditor_view))
        ]
        return my_urls + urls

    @staticmethod
    def get_add_urls(models, task_id):
        return ['%s?task=%s' %
                (reverse('admin:%s_%s_add' % (model._meta.app_label,
                                              model._meta.model_name)),
                 task_id)
                for model in models]

    def add_step_view(self, request, task_id):
        available_step_models = [apps.get_model('survey', model_name)
                                 for model_name in NAME_TO_STEP.values()]
        available_step_urls = self.get_add_urls(available_step_models, task_id)
        context = dict(
            self.admin_site.each_context(request),
            step_urls=available_step_urls
        )

        return TemplateResponse(request, self.step_add_template, context)

    def add_auditor_view(self, request, task_id):
        available_auditor_models = []
        for model_name in NAME_TO_AUDITOR.values():
            model = apps.get_model('survey', model_name)
            if model.objects.filter(task=task_id).count() == 0:
                available_auditor_models.append(model)
        available_auditor_urls = self.get_add_urls(available_auditor_models,
                                                   task_id)
        context = dict(
            self.admin_site.each_context(request),
            auditor_urls=available_auditor_urls
        )

        return TemplateResponse(request, self.auditor_add_template, context)

    def get_models_change_pages(self, models):
        links = []
        for model in models:
            links.append(reverse('admin:%s_%s_change' %
                                 (model._meta.app_label,
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
