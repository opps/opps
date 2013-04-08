#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sites.models import get_current_site
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import Http404

from haystack.views import SearchView

from .models import Post
from opps.channels.models import Channel
from opps.core.models import OppsDetail, OppsList


class PostDetail(OppsDetail):
    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        self.type = 'articles'
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


class PostList(OppsList):
    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        self.type = "channels"
        self.long_slug = None
        if not self.kwargs.get('channel__long_slug'):
            self.article = Post.objects.filter(channel__homepage=True,
                                               site=self.site,
                                               date_available__lte=timezone.
                                               now(),
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
