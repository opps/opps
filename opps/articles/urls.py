#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.conf import settings

from opps.core.cache import cache_page

from .views import AlbumList
from .views import AlbumChannelList


urlpatterns = patterns(
    '',
    url(r'^albums/$',
        cache_page(settings.OPPS_CACHE_EXPIRE_LIST)(
            AlbumList.as_view()), name='album_list'),

    url(r'^album/(?P<channel__long_slug>[\w\b//-]+)/$',
        cache_page(settings.OPPS_CACHE_EXPIRE_LIST)(
            AlbumChannelList.as_view()), name='album_channel'),
)
