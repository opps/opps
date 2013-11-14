#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication

from .models import Logging as LoggingModel


class Logging(ModelResource):
    class Meta:
        allowed_methods = ['post']
        queryset = LoggingModel.objects.filter(
            published=True,
            date_available__lte=timezone.now()
        )
        authentication = ApiKeyAuthentication()
