from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submission/(?P<pk>[0-9]+)/$', views.RecordSubmission.as_view(),
        name='recordSubmission'),
    url(r'^task/(?P<pk>[0-9]+)/$', views.TaskView.as_view(),
        name='TaskPage')
]
