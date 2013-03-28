#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.sites.models import get_current_site
from django.core.paginator import Paginator, InvalidPage
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import Http404
from django.conf import settings

from haystack.views import SearchView

from .models import Post
from opps.channels.models import Channel


def set_context_data(self, SUPER, **kwargs):
    context = super(SUPER, self).get_context_data(**kwargs)
    if len(self.article) >= 1:
        article = self.article.get()
        context['opps_channel'] = article.channel
        context['opps_channel_conf'] = settings.OPPS_CHANNEL_CONF\
                .get(article.channel.slug, '')
    return context


class OppsList(ListView):

    context_object_name = "context"

    def get_context_data(self, **kwargs):
        return set_context_data(self, OppsList, **kwargs)

    @property
    def template_name(self):
        homepage = Channel.objects.get_homepage(site=self.site)
        if not homepage:
            return None

        long_slug = self.kwargs.get('channel__long_slug',
                                    homepage.long_slug)
        if homepage.long_slug != long_slug:
            long_slug = long_slug[:-1]

        domain_folder = 'channels'
        if self.site.id > 1:
            domain_folder = "{0}/channels".format(self.site)

        return '{0}/{1}.html'.format(domain_folder, long_slug)

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        if not self.kwargs.get('channel__long_slug'):
            self.article = Post.objects.filter(channel__homepage=True,
                                               site=self.site,
                                               date_available__lte=timezone.now(),
                                               published=True).all()
            return self.article
        long_slug = self.kwargs['channel__long_slug'][:-1]
        get_object_or_404(Channel, site=self.site, long_slug=long_slug,
                          date_available__lte=timezone.now(), published=True)
        self.article = Post.objects.filter(site=self.site,
                                           channel__long_slug=long_slug,
                                           date_available__lte=timezone.now(),
                                           published=True).all()
        return self.article


class OppsDetail(DetailView):

    context_object_name = "context"

    def get_context_data(self, **kwargs):
        return set_context_data(self, OppsDetail, **kwargs)

    @property
    def template_name(self):
        homepage = Channel.objects.get_homepage(site=self.site)
        if not homepage:
            return None
        long_slug = self.kwargs.get('channel__long_slug', homepage.long_slug)

        domain_folder = 'articles'
        if self.site.id > 1:
            domain_folder = "{0}/articles".format(self.site)

        return '{0}/{1}.html'.format(domain_folder,
                                     long_slug)

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        homepage = Channel.objects.get_homepage(site=self.site)
        slug = None
        if homepage:
            slug = homepage.long_slug
        long_slug = self.kwargs.get('channel__long_slug', slug)
        self.article = Post.objects.filter(site=self.site,
                                   channel__long_slug=long_slug,
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
