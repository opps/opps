#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from opps.api import BaseHandler

from .models import Logging


class LoggingHandler(BaseHandler):
    allowed_methods = ('POST', 'GET')
    model = Logging

    def create(self, request):
        method = getattr(request, request.method)

        User = get_user_model()
        username = method.get('api_username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return {}

        try:
            site = Site.objects.get(domain=method.get('site'))
        except Site.DoesNotExist:
            site = Site.objects.order_by('id')[0]

        log = Logging.objects.create(
            user=user,
            site=site,
            application=method.get('application'),
            action=method.get('action'),
            text=method.get('text'),
        )
        return log
