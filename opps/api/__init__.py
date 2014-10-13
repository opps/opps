#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from piston.handler import BaseHandler as Handler
from piston.emitters import JSONEmitter, Emitter

from opps.api.models import ApiKey


class UncachedEmitter(JSONEmitter):
    """ In websites running under varnish or another cache
    caching the api can mess the results and return the wrong data
    this emmitter injects No-Cache headers in response"""

    def render(self, request):
        content = super(UncachedEmitter, self).render(request)
        response = HttpResponse(content)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Content-Type'] = 'application/json; charset=utf-8'
        response['Pragma'] = 'no-cache'
        response['Expires'] = 0
        return response

Emitter.register('json', UncachedEmitter, 'application/json; charset=utf-8')


class BaseHandler(Handler):
    limit = 20
    limit_arg = 'paginate_limit'
    meta = {}

    blackfield = ['num_pages', 'page_range', 'total_objects', 'per_page',
                  'page', 'has_next', 'has_previous', 'has_other_pages',
                  'end_index', 'start_index', 'start_index']

    def include_meta(self, d):
        obj = {'meta': self.meta, 'objects': d}
        return obj

    def paginate_queryset(self, queryset, request):
        limit = request.GET.get(self.limit_arg, self.meta.get(self.limit_arg))
        paginator = Paginator(queryset, limit or self.limit)

        self.meta['num_pages'] = paginator.num_pages
        self.meta['page_range'] = paginator.page_range
        self.meta['total_objects'] = paginator.count
        self.meta['per_page'] = paginator.per_page

        page = self.meta.get('page', request.GET.get('page', 1))

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        self.meta['has_next'] = results.has_next()
        self.meta['has_previous'] = results.has_previous()
        self.meta['has_other_pages'] = results.has_other_pages()
        self.meta['end_index'] = results.end_index()
        self.meta['start_index'] = results.start_index()
        self.meta['page_number'] = results.number

        return results

    def read(self, request):
        base = self.model.objects

        if request.GET.items():
            items = request.GET.dict()
            self.meta[self.limit_arg] = items.pop(self.limit_arg, None)
            self.meta['page'] = items.pop('page', 1)
            qs = base.filter(**items)
        else:
            qs = base.all()

        self.meta['total_objects'] = qs.count()
        return qs

    def _limit(self, request):
        limit = request.GET.get(self.limit_arg, self.limit)
        return int(limit) * int(request.GET.get('page', 1))

    def _page(self, request):
        page = int(request.GET.get('page', 1))
        if page == 1:
            return 0
        limit = int(request.GET.get(self.limit_arg, self.limit))
        return limit * page - page

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
