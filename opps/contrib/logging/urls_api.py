#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.conf import settings

from tastypie.api import Api

from .api import Logging

print settings.OPPS_API_NAME
_api = Api(
    api_name=u"{}/contrib".format(settings.OPPS_API_NAME))
_api.register(Logging())


urlpatterns = patterns(
    '',
    url(r'^api/', include(_api.urls)),
)
