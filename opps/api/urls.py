#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
)
