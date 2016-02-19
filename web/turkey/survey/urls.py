from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^stepData/(?P<name>[A-z0-9]+)/(?P<pk>[0-9]+)/$', views.RecordStepData,
        name='recordStep')
]
