#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from piston.resource import Resource

from opps.containers.api import ContainerHandler, ContainerBoxHandler


container = Resource(handler=ContainerHandler)
containerbox = Resource(handler=ContainerBoxHandler)

urlpatterns = patterns(
    '',
    url(r'^container/$', container, {'emitter_format': 'json'}),
    url(r'^containerbox/$', containerbox, {'emitter_format': 'json'}),
)
