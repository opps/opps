#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.conf import settings

from opps.core.cache import cache_page

from .views import AsyncServer, LongPullingServer


urlpatterns = patterns(
    '',
    url(r'^(?P<channel__long_slug>[\w//-]+)/(?P<slug>[\w-]+)\.server$',
        cache_page(settings.OPPS_CACHE_EXPIRE_DETAIL)(
            AsyncServer.as_view()), name='asyncserver'),
    url(r'^(?P<channel__long_slug>[\w//-]+)/(?P<slug>[\w-]+)\.pulingserver$',
        cache_page(settings.OPPS_CACHE_EXPIRE_DETAIL)(
            LongPullingServer.as_view()), name='pulingserver'),
)
