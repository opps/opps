#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from opps.core.cache import cache_page

from .views import PageDetail


urlpatterns = patterns(
    '',

    # FLATPAGEs
    url(r'^page/(?P<slug>[\w\b//-]+)/$',
        cache_page(60 * 2)(PageDetail.as_view()), name='open'),
)
