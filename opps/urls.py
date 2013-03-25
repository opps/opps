#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf.urls import patterns, url, include


urlpatterns = patterns(
    '',
    url(r'^redactor/', include('redactor.urls')),
    url(r'^sitemap.xml', include('static_sitemaps.urls')),
    url(r'^', include('opps.articles.urls', namespace='articles',
                      app_name='articles')),
)
