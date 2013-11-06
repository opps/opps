#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from tastypie.api import Api

from opps.containers.api import Container, ContainerBox
from opps.containers.api import ContainerBoxItens
from opps.articles.api import Post, Album, Link

from .conf import settings


_api = Api(api_name=settings.OPPS_API_NAME)
_api.register(Container())
_api.register(ContainerBox())
_api.register(ContainerBoxItens())
_api.register(Post())
_api.register(Album())
_api.register(Link())


urlpatterns = patterns(
    '',
    url(r'^', include(_api.urls)),
)
