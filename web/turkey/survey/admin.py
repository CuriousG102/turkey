from django.conf.urls import url
from django.contrib import admin
from django.apps import apps
from django.contrib.admin.options import IS_POPUP_VAR, TO_FIELD_VAR
from django.contrib.admin.utils import unquote, get_deleted_objects
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
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

        def redirect_back_to_task(self, request, task_id):
            return redirect('admin:survey_task_change', task_id)

        def delete_view(self, request, object_id, extra_context=None):
            to_field = request.POST.get(TO_FIELD_VAR,
                                        request.GET.get(TO_FIELD_VAR))
            # parent raises exception under these conditions before obj is
            # obtained, so we preserve that ordering here
            if not (to_field and not self.to_field_allowed(request, to_field)):
                obj = self.get_object(request, unquote(object_id), to_field)
                if obj is not None:
                    task_id = obj.task.pk

            # by calling parent here, we can get the object's associated task
            # before it is deleted, but let the parent do all necessary
            # handling and give it an opportunity to generate exceptions
            parent_response = super().delete_view(request, object_id,
                                                  extra_context)

            # request.post means user has confirmed deletion, this is the
            # response we potentially wish to redirect
            if request.POST and IS_POPUP_VAR not in request.POST:
                # Your IDE will warn you that task_id may be referenced before
                # assignment. This is not possible because the conditions
                # that would cause task_id not to be assigned would also
                # cause the parent call to raise an exception
                return self.redirect_back_to_task(request, task_id)

            return parent_response

        def response_post_save_change(self, request, obj):
            return self.redirect_back_to_task(request, obj.task.pk)

        def response_post_save_add(self, request, obj):
            return self.redirect_back_to_task(request, obj.task.pk)

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
    actions = ['export_tasks_data']

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

        embed_uri = request.build_absolute_uri(
            static('survey/js/mmm_turkey.js'))
        task_id = task.pk if task is not None else None
        auditor_uris = []
        for auditor in related_auditor_models:
            auditor_loc = static(auditor.script_location)
            auditor_uri = request.build_absolute_uri(auditor_loc)
            auditor_uris.append(auditor_uri)

        fetch_interaction_endpoint = request.build_absolute_uri(
            reverse('survey:create_interaction'))

        if task is not None:
            embed_code = render_to_string(
                'survey/admin/embed_template.html',
                {'embed_uri': mark_safe(embed_uri),
                 'submission_endpoint': mark_safe('null'),
                 'fetch_interaction_endpoint': mark_safe('"%s"' % fetch_interaction_endpoint),
                 'task_pk': mark_safe(str(task_id)),
                 'fetch_data': mark_safe('true'),
                 'auditor_uris': auditor_uris},
                request=request)
        else:
            embed_code = ''

        # strip embed_code of its safe status so it is escaped by Django
        # template
        embed_code = str(embed_code).strip('\n')

        context.update({
            'related_steps': related_steps,
            'related_auditors': related_auditors,
            'task_id': task_id if task_id is not None else 0,
            'embed_code': embed_code
        })
        return super().render_change_form(request, context, **kwargs)

    def export_tasks_data(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return redirect('survey:export_tasks', primary_keys=','.join(selected))
