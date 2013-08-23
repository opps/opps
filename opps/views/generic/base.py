#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django import template
from django.conf import settings
from django.contrib.sites.models import get_current_site

from opps.articles.models import Album
from opps.containers.models import Container, ContainerBox
from opps.channels.models import Channel


class View(object):

    context_object_name = "context"
    paginate_by = settings.OPPS_PAGINATE_BY
    limit = settings.OPPS_VIEWS_LIMIT

    def __init__(self):
        self.slug = None
        self.channel = None
        self.long_slug = None
        self.channel_long_slug = []
        self.article = None
        self.excluded_ids = set()
        self.child_class = u'container'

    def get_paginate_by(self, queryset):
        queryset = self.get_queryset()

        setting_name = 'OPPS_{}_{}_PAGINATE_BY'.format(queryset.
                                                       model._meta.app_label,
                                                       queryset.model.
                                                       __name__).upper()

        paginate_by = getattr(settings, setting_name, self.paginate_by)

        return paginate_by

    def get_context_data(self, **kwargs):
        if not self.long_slug:
            context = []
            return context
        context = super(View, self).get_context_data(**kwargs)

        # channel is needed everywhere
        self.channel = self.channel or Channel.objects.get_homepage(
            site=get_current_site(self.request)
        )

        if hasattr(self, 'articleboxes'):
            context['articleboxes'] = self.articleboxes
        else:
            context['articleboxes'] = ContainerBox.objects.filter(
                channel__long_slug=self.long_slug)
            self.excluded_ids = []
            for box in context['articleboxes']:
                self.excluded_ids += [a.pk for a in box.ordered_containers()]

        filters = {}
        filters['site_domain'] = self.site.domain
        filters['channel_long_slug__in'] = self.channel_long_slug
        filters['date_available__lte'] = timezone.now()
        filters['published'] = True
        filters['show_on_root_channel'] = True
        article = Container.objects.filter(**filters)

        context['posts'] = article.filter(
            child_class='Post'
        ).exclude(pk__in=self.excluded_ids)[:self.limit]

        context['albums'] = Album.objects.filter(
            **filters
        ).exclude(pk__in=self.excluded_ids)[:self.limit]

        context['channel'] = {}
        context['channel']['long_slug'] = self.long_slug
        if self.channel:
            context['channel'] = self.channel

        if self.slug:
            context['articleboxes'] = context['articleboxes'].filter(
                containers__slug=self.slug)

        return context

    def get_template_folder(self):
        domain_folder = "containers"
        if settings.SITE_ID > 1:
            domain_folder = "{}/containers".format(self.request.site.domain)
        return domain_folder

    def get_long_slug(self):
        self.long_slug = self.kwargs.get('channel__long_slug', None)
        try:
            if not self.long_slug:
                self.long_slug = Channel.objects.get_homepage(
                    site=self.site).long_slug
        except AttributeError:
            pass
        return self.long_slug

    def set_channel_rules(self):
        self.channel = get_object_or_404(Channel,
                                         site__domain=self.site.domain,
                                         long_slug=self.long_slug,
                                         date_available__lte=timezone.now(),
                                         published=True)
        self.long_slug = self.channel.long_slug

        self.channel_long_slug = [self.long_slug]
        for children in self.channel.get_children():
            self.channel_long_slug.append(children.long_slug)

    def check_template(self, _template):
        try:
            template.loader.get_template(_template)
            return True
        except template.TemplateDoesNotExist:
            return False
