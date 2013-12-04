#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth import authenticate

from piston.handler import BaseHandler as Handler

from opps.api.models import ApiKey


class BaseHandler(Handler):

    def read(self, request):
        base = self.model.objects
        if request.GET.items():
            return base.filter(**request.GET.dict())
        return base.all()


class ApiKeyAuthentication(object):
    def __init__(self, auth_func=authenticate, method=['GET']):
        self.auth_func = auth_func
        self.method = method

    def is_authenticated(self, request):
        if request.method == 'GET' and 'GET' in self.method:
            return True

        method = getattr(request, request.method)
        try:
            key = ApiKey.objects.get(
                user__username=method.get('api_username'),
                key=method.get('api_key'))
        except ApiKey.DoesNotExist:
            return False

        import pdb; pdb.set_trace()
        user = self.auth_func(username=key.user.username,
                              password=key.user.password)

        if not user:
            return False

        return request.user.is_authenticated()

    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp.status_code = 401
        return resp
