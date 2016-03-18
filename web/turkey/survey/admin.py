from django.conf.urls import url
from django.contrib import admin
from django.apps import apps
from django.contrib.admin.options import IS_POPUP_VAR
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from .models import Task
from .steps import NAME_TO_STEP
from .auditors import NAME_TO_AUDITOR


def create_step_or_auditor_admin(model):
    model_inlines = []
    for inline in model.inlines:
        class Inline(admin.StackedInline):
            model = apps.get_model('survey', inline)
            extra = 0

        model_inlines.append(Inline)

    class StepAuditorAdmin(admin.ModelAdmin):
        inlines = model_inlines  # autogenerate inlines as well

        def get_model_perms(self, request):
            # hacky way to keep this
            # from showing up in the list of models
            return {}

        def redirect_back_to_task(self, request, obj):
            POST = request.POST
            # if this looks messy it's because Django framework's ModelAdmin
            # code is apparently also a train wreck
            if IS_POPUP_VAR in POST or '_continue' in POST \
                    or '_addanother' in POST:
                return None
            return redirect('admin:survey_task_change', obj.task.pk)

        def response_change(self, request, obj):
            return self.redirect_back_to_task(request, obj) \
                   or super().response_change(request, obj)

        def response_add(self, request, obj, post_url_continue=None):
            return self.redirect_back_to_task(request, obj) \
                   or super().response_add(request, obj,
                                           post_url_continue=post_url_continue)

    admin.site.register(model, StepAuditorAdmin)


def create_step_or_auditor_admins(model_name_list):
    for model_name in model_name_list:
        model = apps.get_model('survey', model_name)
        if not model.has_custom_admin:
            create_step_or_auditor_admin(model)


create_step_or_auditor_admins(NAME_TO_STEP.values())
create_step_or_auditor_admins(NAME_TO_AUDITOR.values())


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    step_add_template = 'survey/admin/step_add.html'
    auditor_add_template = 'survey/admin/auditor_add.html'

    def get_urls(self):
        urls = super().get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name
        my_urls = [
            url(r'^(?P<task_id>[0-9]+)/add_step/$',
                self.admin_site.admin_view(self.add_step_view,
                                           cacheable=True),
                name='%s_%s_add_step' % info),
            url(r'^(?P<task_id>[0-9]+)/add_auditor/$',
                self.admin_site.admin_view(self.add_auditor_view),
                name='%s_%s_add_auditor' % info)
        ]
        return my_urls + urls

    @staticmethod
    def get_add_urls(models, task_id):
        return ['%s?task=%s' %
                (reverse('admin:%s_%s_add' % (model._meta.app_label,
                                              model._meta.model_name)),
                 task_id)
                for model in models]

    def convert_and_check_task_id(self, task_id):
        if task_id == 0:
            raise Http404(
                _('Cannot add %s to an %s that does not '
                  'yet exist' %
                  ('steps', self.model._meta.verbose_name.title()))
            )
        try:
            task_id = int(task_id)
        except ValueError:
            raise Http404(_('%s not a primary key') % task_id)
        try:
            self.model.objects.get(pk=task_id)
        except self.model.DoesNotExist:
            raise Http404(_('%s with pk %d does not exist') %
                          (self.model._meta.verbose_name.title(), task_id))
        return task_id

    def add_step_view(self, request, task_id=None):
        task_id = self.convert_and_check_task_id(task_id)
        available_step_models = [apps.get_model('survey', model_name)
                                 for model_name in NAME_TO_STEP.values()]
        return self.get_add_page_response(request, self.step_add_template,
                                          available_step_models, task_id)

    def add_auditor_view(self, request, task_id=None):
        task_id = self.convert_and_check_task_id(task_id)
        available_auditor_models = []
        for model_name in NAME_TO_AUDITOR.values():
            model = apps.get_model('survey', model_name)
            if model.objects.filter(task=task_id).count() == 0:
                available_auditor_models.append(model)
        return self.get_add_page_response(request, self.auditor_add_template,
                                          available_auditor_models, task_id)

    def get_add_page_response(self, request, template, models, task_id):
        names = [model._meta.verbose_name.title for model in models]
        urls = self.get_add_urls(models, task_id)
        context = dict(
            self.admin_site.each_context(request),
            model_names_and_urls=zip(names, urls)
        )
        return TemplateResponse(request, template, context)

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
            'related_auditors': related_auditors,
            'task_id': task.pk if task is not None else 0
        })
        return super().render_change_form(request, context, **kwargs)
