from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submission/(?P<pk>[0-9]+)/$', views.RecordSubmission.as_view(),
        name='recordSubmission'),
]
