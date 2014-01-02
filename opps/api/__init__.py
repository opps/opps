#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth import authenticate

from piston.handler import BaseHandler as Handler

from opps.api.models import ApiKey


class BaseHandler(Handler):
    limit = 20

    def dispatch(self, request):
        import pdb; pdb.set_trace()
        pass

    def read(self, request):
        base = self.model.objects
        if request.GET.items():
            items = request.GET.dict()
            if request.GET.get('paginate_limit'):
                del items['paginate_limit']
            if request.GET.get('page'):
                del items['page']
            return base.filter(**items)
        return base.all()

    def _limit(self, request):
        limit = request.GET.get('paginate_limit', self.limit)
        return int(limit)*int(request.GET.get('page', 1))

    def _page(self, request):
        page = int(request.GET.get('page', 1))
        if page == 1:
            return 0
        limit = int(request.GET.get('paginate_limit', self.limit))
        return limit*page-page

    def appendModel(Model, Filters):
        m = Model.objects.filter(**Filters)
        l = []
        for i in m:
            l.append(i.__dict__)
        return l


class ApiKeyAuthentication(object):
    def __init__(self, auth_func=authenticate, method=['GET']):
        self.auth_func = auth_func
        self.method = method

    def is_authenticated(self, request):
        if request.method == 'GET' and 'GET' in self.method:
            return True

        try:
            method = getattr(request, request.method)
        except:
            method = request.GET

        try:
            ApiKey.objects.get(
                user__username=method.get('api_username'),
                key=method.get('api_key'))
        except ApiKey.DoesNotExist:
            return False

        return True

    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp.status_code = 401
        return resp
