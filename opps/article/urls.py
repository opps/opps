#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf.urls import patterns, url, include

from opps.article.views import OppsDetail, OppsList


urlpatterns = patterns('',
        url(r'^redactor/', include('redactor.urls')),
        url(r'^$', OppsList.as_view(), name='home'),
        url(r'^(?P<channel__long_slug>[\w//-]+)/(?P<slug>[\w-]+)$',
            OppsDetail.as_view(), name='open'),
        url(r'^(?P<channel__long_slug>[\w//-]+)$',
            OppsList.as_view(), name='channel'),
)
