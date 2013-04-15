#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from django.contrib.sites.models import get_current_site
from django import template
from django.utils import timezone

from .models import FlatPage


class PageDetail(DetailView):

    model = FlatPage
    context_object_name = "context"
    type = 'pages'

    @property
    def template_name(self):
        domain_folder = self.type
        if self.site.id > 1:
            domain_folder = "{0}/{1}".format(self.site, self.type)

        try:
            _template = '{0}/{1}.html'.format(
                domain_folder, self.page.get().slug)
            template.loader.get_template(_template)
        except template.TemplateDoesNotExist:
            _template = '{0}.html'.format(domain_folder)
        return _template

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        self.slug = self.kwargs.get('slug')

        self.page = self.model.objects.filter(
            site=self.site,
            slug=self.slug,
            date_available__lte=timezone.now(),
            published=True)
        return self.page
