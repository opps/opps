#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import GetImagesView

urlpatterns = patterns(
    '',
    url(r'^image_add/', 'opps.images.views.image_add', name='image_add'),
    url(r'^get_images/', GetImagesView.as_view(), name='get_images'),
)
