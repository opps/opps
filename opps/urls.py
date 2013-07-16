#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from opps.contrib import admin
from admin.plugins import xversion


admin.autodiscover()
xversion.registe_models()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^redactor/', include('redactor.urls')),

    url(r'^sitemap', include('opps.sitemaps.urls')),

    url(r'^', include('opps.containers.urls', namespace='containers',
                      app_name='containers')),
)
