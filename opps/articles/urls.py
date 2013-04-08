#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

from .views import OppsDetail, PostList, Search


urlpatterns = patterns(
    '',
    url(r'^$', cache_page(60 * 2)(PostList.as_view()), name='home'),
    url(r'^search/', Search(), name='search'),
    url(r'^(?P<channel__long_slug>[\w//-]+)/(?P<slug>[\w-]+)$',
        cache_page(60 * 15)(OppsDetail.as_view()), name='open'),
    url(r'^(?P<channel__long_slug>[\w\b//-]+)/$',
        cache_page(60 * 2)(PostList.as_view()), name='channel'),
)
