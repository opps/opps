#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils import timezone
from django import template
from django.conf import settings

from opps.articles.utils import set_context_data
from opps.channels.models import Channel


class OppsList(ListView):

    context_object_name = "context"
    paginate_by = settings.OPPS_PAGINATE_BY
    limit = settings.OPPS_VIEWS_LIMIT
    slug = None

    def get_context_data(self, **kwargs):
        return set_context_data(self, OppsList, **kwargs)

    @property
    def template_name(self):
        domain_folder = self.type
        if self.site.id > 1:
            domain_folder = "{0}/{1}".format(self.site, self.type)

        if self.channel:
            if self.channel.group and self.channel.parent:
                try:
                    _template = '{0}/_{1}.html'.format(
                        domain_folder, self.channel.parent.long_slug)
                    template.loader.get_template(_template)
                    return _template
                except template.TemplateDoesNotExist:
                    pass

        return '{0}/{1}.html'.format(domain_folder, self.long_slug)

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        try:
            self.long_slug = self.kwargs.get(
                'channel__long_slug',
                Channel.objects.get_homepage(site=self.site).long_slug)
        except AttributeError:
            self.long_slug = None
            return None

        self.channel = get_object_or_404(Channel, site=self.site,
                                         long_slug=self.long_slug,
                                         date_available__lte=timezone.now(),
                                         published=True)

        self.channel_long_slug = [self.long_slug]
        for children in self.channel.get_children():
            self.channel_long_slug.append(children)
        self.article = self.model.objects.filter(
            site=self.site,
            channel_long_slug__in=self.channel_long_slug,
            date_available__lte=timezone.now(),
            published=True)[:self.limit]

        if len(self.article) == 0 and self.kwargs.get('channel__long_slug',
                                                      None):
            raise Http404

        return self.article


class OppsDetail(DetailView):

    context_object_name = "context"
    limit = settings.OPPS_VIEWS_LIMIT

    def get_context_data(self, **kwargs):
        return set_context_data(self, OppsDetail, **kwargs)

    @property
    def template_name(self):
        domain_folder = self.type
        if self.site.id > 1:
            domain_folder = "{0}/{1}".format(self.site, self.type)
        try:
            _template = '{0}/{1}/{2}.html'.format(
                domain_folder, self.long_slug, self.slug)
            template.loader.get_template(_template)
        except template.TemplateDoesNotExist:
            _template = '{0}/{1}.html'.format(domain_folder, self.long_slug)
        return _template

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        self.slug = self.kwargs.get('slug')

        try:
            self.long_slug = self.kwargs.get(
                'channel__long_slug',
                Channel.objects.get_homepage(site=self.site).long_slug)
        except AttributeError:
            self.long_slug = None
            return None

        self.channel = get_object_or_404(Channel, site=self.site,
                                         long_slug=self.long_slug,
                                         date_available__lte=timezone.now(),
                                         published=True)

        self.channel_long_slug = [self.long_slug]
        self.channel_long_slug.append(
            [children.long_slug for children in self.channel.get_children()])

        self.article = self.model.objects.filter(
            site=self.site,
            channel_long_slug=self.long_slug,
            slug=self.slug,
            date_available__lte=timezone.now(),
            published=True)
        return self.article
