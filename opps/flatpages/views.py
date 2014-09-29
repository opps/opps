#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from django.contrib.sites.models import get_current_site
from django.db.models import Q
from django.utils import timezone

from .models import FlatPage


class PageDetail(DetailView):

    model = FlatPage
    context_object_name = "context"
    type = 'flatpages'

    def get_template_names(self):
        _template_names = super(PageDetail, self).get_template_names()

        template_names = []

        base_path = '{}/{}.html'.format(self.type, self.page.get().slug)

        if self.site.id > 1:
            template_names.append('{}/{}'.format(self.site, base_path))

        template_names.append(base_path)

        return template_names + _template_names

    def get_queryset(self):
        self.site = get_current_site(self.request)
        self.slug = self.kwargs.get('slug')

        self.page = self.model.objects.filter(
            Q(global_page=True) | Q(site=self.site),
            slug=self.slug,
            date_available__lte=timezone.now(),
            published=True)
        return self.page
