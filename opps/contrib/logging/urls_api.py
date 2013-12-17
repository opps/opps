#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from piston.resource import Resource

from opps.api import ApiKeyAuthentication

from .api import LoggingHandler


logging = Resource(handler=LoggingHandler,
                   authentication=ApiKeyAuthentication())

urlpatterns = patterns(
    '',
    url(r'^api/contrib/logging/$', logging, {'emitter_format': 'json'}),
)
