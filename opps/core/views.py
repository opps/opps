#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django import template

from .utils import set_context_data


class OppsList(ListView):

    context_object_name = "context"

    def get_context_data(self, **kwargs):
        return set_context_data(self, OppsList, **kwargs)

    @property
    def template_name(self):
        domain_folder = self.type
        if self.site.id > 1:
            domain_folder = "{0}/{1}".format(self.site, self.type)

        return '{0}/{1}.html'.format(domain_folder, self.long_slug)


class OppsDetail(DetailView):

    context_object_name = "context"

    def get_context_data(self, **kwargs):
        return set_context_data(self, OppsDetail, **kwargs)

    @property
    def template_name(self):
        domain_folder = self.type
        if self.site.id > 1:
            domain_folder = "{0}/{1}".format(self.site, self.type)
        try:
            _template = '{0}/{1}/{2}.html'.format(
                domain_folder, self.long_slug, self.article.get().slug)
            template.loader.get_template(_template)
        except template.TemplateDoesNotExist:
            _template = '{0}/{1}.html'.format(domain_folder, self.long_slug)
        return _template
