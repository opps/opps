#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django import template
from django.conf import settings

from opps.articles.models import ArticleBox, Article, Album
from opps.channels.models import Channel


class OppsView(object):

    context_object_name = "context"
    paginate_by = settings.OPPS_PAGINATE_BY
    limit = settings.OPPS_VIEWS_LIMIT

    def __init__(self):
        self.slug = None
        self.channel = None
        self.long_slug = None
        self.channel_long_slug = []
        self.article = self.model.objects.select_related('publisher')

    def get_context_data(self, **kwargs):
        context = super(OppsView, self).get_context_data(**kwargs)

        filters = {}
        filters['site'] = self.site
        filters['channel_long_slug__in'] = self.channel_long_slug
        filters['date_available__lte'] = timezone.now()
        filters['published'] = True
        article = Article.objects.filter(**filters)
        context['posts'] = article.filter(child_class='Post')[:self.limit]
        context['albums'] = Album.objects.filter(**filters)[:self.limit]

        context['channel'] = {}
        context['channel']['long_slug'] = self.long_slug
        if self.channel:
            context['channel']['slug'] = self.channel.slug
            context['channel']['level'] = self.channel.get_level()
            context['channel']['root'] = self.channel.get_root()

        context['articleboxes'] = ArticleBox.objects.filter(
            channel__long_slug=self.long_slug)
        if self.slug:
            context['articleboxes'] = context['articleboxes'].filter(
                article__slug=self.slug)

        return context

    def get_template_folder(self):
        domain_folder = self.type
        if self.site.id > 1:
            domain_folder = "{0}/{1}".format(self.site, self.type)
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
        self.channel = get_object_or_404(Channel, site=self.site,
                                         long_slug=self.long_slug,
                                         date_available__lte=timezone.now(),
                                         published=True)

        self.channel_long_slug = [self.long_slug]
        for children in self.channel.get_children():
            self.channel_long_slug.append(children)

    def check_template(self, _template):
        try:
            template.loader.get_template(_template)
            return True
        except template.TemplateDoesNotExist:
            return False


class OppsList(OppsView, ListView):

    def get_template_names(self):
        names = []
        domain_folder = self.get_template_folder()

        if self.channel:
            if self.channel.group and self.channel.parent:

                _template = '{}/_{}.html'.format(
                    domain_folder, self.channel.parent.long_slug)
                if self.check_template(_template):
                    names.append(_template)

                _template = '{}/_post_list.html'.format(
                    domain_folder, self.channel.parent.long_slug)
                if self.check_template(_template):
                    names.append(_template)

        names.append('{}/{}.html'.format(domain_folder, self.long_slug))

        try:
            names = names + super(OppsList, self).get_template_names()
        except ImproperlyConfigured:
            pass

        return names

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        self.long_slug = self.get_long_slug()

        if not self.long_slug:
            return None

        self.set_channel_rules()

        self.article = self.model.objects.filter(
            site=self.site,
            channel_long_slug__in=self.channel_long_slug,
            date_available__lte=timezone.now(),
            published=True).select_related('publisher')[:self.limit]

        return self.article


class OppsDetail(OppsView, DetailView):

    def get_template_names(self):
        names = []
        domain_folder = self.get_template_folder()

        names.append('{}/{}/{}.html'.format(
            domain_folder, self.long_slug, self.slug))
        names.append('{}/{}.html'.format(domain_folder, self.long_slug))

        try:
            names = names + super(OppsDetail, self).get_template_names()
        except ImproperlyConfigured:
            pass

        return names

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        self.slug = self.kwargs.get('slug')
        self.long_slug = self.get_long_slug()
        if not self.long_slug:
            return None

        self.set_channel_rules()

        self.article = self.model.objects.filter(
            site=self.site,
            channel_long_slug=self.long_slug,
            slug=self.slug,
            date_available__lte=timezone.now(),
            published=True).select_related('publisher')
        return self.article
