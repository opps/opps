#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from rest_framework import routers

from opps.containers.views import ContainerAPIList, ContainerAPIDetail


router = routers.DefaultRouter()

urlpatterns = patterns(
    '',
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^(?P<channel__long_slug>[\w//-]+)/(?P<slug>[\w-]+)\.html$',
        ContainerAPIDetail.as_view(), name='container'),

    url(r'^(?P<channel__long_slug>[\w\b//-]+)/$',
        ContainerAPIList.as_view(), name='channel'),

    url(r'^', include(router.urls)),

)
