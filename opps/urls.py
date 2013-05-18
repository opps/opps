#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^redactor/', include('redactor.urls')),

    url(r'^sitemap', include('opps.sitemaps.urls')),
    url(r'^page/', include('opps.flatpages.urls', namespace='pages',
                           app_name='pages')),
    url(r'^', include('opps.articles.urls', namespace='articles',
                      app_name='articles')),
)
