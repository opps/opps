#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^fileupload/', include('opps.contrib.fileupload.urls')),

    url(r'^sitemap', include('opps.sitemaps.urls')),

    url(r'^api/', include('opps.api.urls')),

    url(r'^', include('opps.containers.urls', namespace='containers',
                      app_name='containers')),
)
