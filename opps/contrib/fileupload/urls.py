from django.conf.urls import patterns
from .views import image_create

urlpatterns = patterns(
    '',
    (r'^image/(?P<container_pk>\d+)/$', image_create, {}, 'upload-new'),
)
