#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

from .views import PostDetail, PostList, AlbumList, AlbumDetail, TagList
from .views import Search


urlpatterns = patterns(
    '',
    url(r'^$', cache_page(60 * 2)(PostList.as_view()), name='home'),
    url(r'^search/', Search(), name='search'),

    # ALBUM
    url(r'^album/(?P<channel__long_slug>[\w\b//-]+)/$',
        cache_page(60 * 2)(AlbumList.as_view()), name='album_channel'),
    url(r'^album/(?P<channel__long_slug>[\w//-]+)/(?P<slug>[\w-]+)$',
        cache_page(60 * 15)(AlbumDetail.as_view()), name='album_open'),

    # TAGs
    url(r'^tag/(?P<tag>[\w//-]+)$',
        cache_page(60 * 2)(TagList.as_view()), name='tag_open'),

    # POST
    url(r'^(?P<channel__long_slug>[\w//-]+)/(?P<slug>[\w-]+)$',
        cache_page(60 * 15)(PostDetail.as_view()), name='open'),
    url(r'^(?P<channel__long_slug>[\w\b//-]+)/$',
        cache_page(60 * 2)(PostList.as_view()), name='channel'),
)
