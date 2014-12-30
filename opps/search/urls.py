# coding: utf-8
try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

from .views import SearchOrdered

urlpatterns = patterns(
    'haystack.views',
    url(r'^$', SearchOrdered(),
        name='haystack_search'),
)
