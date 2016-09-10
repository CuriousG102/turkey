from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submission/(?P<pk>[0-9]+)/$', views.RecordSubmission.as_view(),
        name='recordSubmission'),
    url(r'^task/(?P<pk>[0-9]+)/$', views.TaskView.as_view(),
        name='TaskPage'),
    url(r'^export_tasks/(?P<primary_keys>(\d+,)*\d+)/export.xml',
        views.TasksExport.as_view(),
        name='export_tasks'),
    url(r'^auditor_scripts/(?P<task_pk>[0-9]+)/',
        views.AuditorScriptsView.as_view(),
        name='auditor_scripts'),
]
