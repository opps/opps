#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils import timezone

from opps.api import BaseHandler


from .models import Container
from .models import ContainerBox


class Handler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        filters = {}
        filters['date_available__lte'] = timezone.now()
        filters['published'] = True
        return self.model.objects.filter(
            **filters)[self._page(request):self._limit(request)]


class ContainerHandler(Handler):
    model = Container


class ContainerBoxHandler(Handler):
    model = ContainerBox
    fields = (
        'name',
        'slug',
        'title',
        'title_url',
        'channel',
        ('containers', ())
    )
    exclude = ['queryset']
