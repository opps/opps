#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf.urls.defaults import patterns, url
from django.conf.urls import include

from opps.core.views import OppsDetail



urlpatterns = patterns('',
        url(r'^redactor/', include('redactor.urls')),
        url(r'^(?P<channel__slug_name>[0-9A-Za-z-_.//]+)/(?P<slug>[\w-]+)$',
            OppsDetail.as_view(), name='home'),
)
