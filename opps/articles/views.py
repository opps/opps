#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.sites.models import get_current_site
from django.core.paginator import Paginator, InvalidPage
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django import template
from django.utils import timezone
from django.http import Http404

from haystack.views import SearchView

from .models import Post
from opps.channels.models import Channel
from opps.core.utils import set_context_data


class OppsList(ListView):

    context_object_name = "context"

    def get_context_data(self, **kwargs):
        return set_context_data(self, OppsList, **kwargs)

    @property
    def template_name(self):
        domain_folder = 'channels'
        if self.site.id > 1:
            domain_folder = "{0}/channels".format(self.site)

        return '{0}/{1}.html'.format(domain_folder, self.long_slug)

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        self.long_slug = None
        if not self.kwargs.get('channel__long_slug'):
            self.article = Post.objects.filter(channel__homepage=True,
                                               site=self.site,
                                               date_available__lte=timezone.now(),
                                               published=True).all()
            homepage = Channel.objects.get_homepage(site=self.site)
            if homepage:
                self.long_slug = homepage.long_slug
            return self.article
        self.long_slug = self.kwargs['channel__long_slug']
        self.channel = get_object_or_404(Channel, site=self.site,
                                         long_slug=self.long_slug,
                                         date_available__lte=timezone.now(),
                                         published=True)
        self.article = Post.objects.filter(site=self.site,
                                           channel=self.channel,
                                           date_available__lte=timezone.now(),
                                           published=True).all()
        return self.article


class OppsDetail(DetailView):

    context_object_name = "context"

    def get_context_data(self, **kwargs):
        return set_context_data(self, OppsDetail, **kwargs)

    @property
    def template_name(self):
        domain_folder = 'articles'
        if self.site.id > 1:
            domain_folder = "{0}/articles".format(self.site)
        try:
            _template = '{0}/{1}/{2}.html'.format(
                domain_folder, self.long_slug, self.article.get().slug)
            template.loader.get_template(_template)
        except template.TemplateDoesNotExist:
            _template = '{0}/{1}.html'.format(domain_folder, self.long_slug)
        return _template

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        homepage = Channel.objects.get_homepage(site=self.site)
        slug = None
        if homepage:
            slug = homepage.long_slug
        self.long_slug = self.kwargs.get('channel__long_slug', slug)
        self.article = Post.objects.filter(site=self.site,
                                   channel__long_slug=self.long_slug,
                                   slug=self.kwargs['slug'],
                                   date_available__lte=timezone.now(),
                                   published=True).all()
        return self.article


class Search(SearchView):
    def get_results(self):
        return self.form.search().order_by('-date_available')

    def build_page(self):
        paginator = Paginator(self.results, self.results_per_page)
        try:
            paginator.page(int(self.request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("No such page!")

        return (None, self.results)
