#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.sites.models import get_current_site
from django.core.paginator import Paginator, InvalidPage
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import Http404

from haystack.views import SearchView

from opps.article.models import Post
from opps.channel.models import Channel


class OppsList(ListView):

    context_object_name = "context"

    @property
    def template_name(self):
        homepage = Channel.objects.get_homepage()
        if not homepage:
            return None
        long_slug = self.kwargs.get('channel__long_slug',
                                    homepage.long_slug)
        return 'channel/{0}.html'.format(long_slug)

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        if not self.kwargs.get('channel__long_slug'):
            return Post.objects.filter(channel__homepage=True,
                                       site=self.site,
                                       date_available__lte=timezone.now(),
                                       published=True).all()
        long_slug = self.kwargs['channel__long_slug'][:-1]
        get_object_or_404(Channel, site=self.site, long_slug=long_slug,
                          date_available__lte=timezone.now(), published=True)
        return Post.objects.filter(site=self.site,
                                   channel__long_slug=long_slug,
                                   date_available__lte=timezone.now(),
                                   published=True).all()


class OppsDetail(DetailView):

    context_object_name = "context"

    @property
    def template_name(self):
        homepage = Channel.objects.get_homepage()
        if not homepage:
            return None
        long_slug = self.kwargs.get('channel__long_slug', homepage.long_slug)
        return 'article/{0}/{1}.html'.format(long_slug, self.kwargs['slug'])

    @property
    def queryset(self):
        homepage = Channel.objects.get_homepage()
        slug = None
        if homepage:
            slug = homepage.long_slug
        long_slug = self.kwargs.get('channel__long_slug', slug)
        return Post.objects.filter(channel__long_slug=long_slug,
                                   slug=self.kwargs['slug'],
                                   date_available__lte=timezone.now(),
                                   published=True).all()


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
