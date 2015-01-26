# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from .views import OppsAutocompleteLookup


urlpatterns = patterns(
    '',
    url(r'^grappelli/lookup/autocomplete/$',
        OppsAutocompleteLookup.as_view(),
        name="grp_autocomplete_lookup"),
)
