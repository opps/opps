#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf.urls.defaults import patterns, url
from django.conf.urls import include



urlpatterns = patterns('',
        url(r'^', include('opps.article.urls', namespace='opps_article')),
)
