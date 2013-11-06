#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from tastypie.api import Api

from opps.containers.api import Container
from opps.articles.api import Post


_api = Api(api_name='v1')
_api.register(Container())
_api.register(Post())


urlpatterns = patterns(
    '',
    url(r'^', include(_api.urls)),
)
