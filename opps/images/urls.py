#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import GetImagesView, PopUpImageView

urlpatterns = patterns(
    '',
    url(r'^image_add/',
        login_required(login_url='/admin/')(PopUpImageView.as_view()),
        name='image_add'),
    url(r'^get_images/', GetImagesView.as_view(), name='get_images'),
)
