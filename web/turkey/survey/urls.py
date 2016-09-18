from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/step_submission/(?P<pk>[0-9]+)/$', views.StepSubmission.as_view(),
        name='step_submission'),
    url(r'^api/auditor_submission/(?P<pk>[0-9]+)/$',
        views.AuditorSubmission.as_view(), name='auditor_submission'),
    url(r'^task/(?P<pk>[0-9]+)/$', views.TaskView.as_view(),
        name='TaskPage'),
    url(r'^api/task/create_interaction/$', views.CreateTaskInteractionView.as_view(),
        name='create_interaction'),
    url(r'^export_tasks/(?P<primary_keys>(\d+,)*\d+)/export.xml',
        views.TasksExport.as_view(),
        name='export_tasks'),
]
