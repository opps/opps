#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage
from django.contrib.sites.models import get_current_site
from django.utils import timezone
from django.http import Http404
from django.conf import settings

from haystack.views import SearchView

from opps.articles.models import Post, Album
from opps.containers.models import Container
from opps.containers.models import ContainerBox

from opps.views.generic.list import ListView
from opps.views.generic.detail import DetailView


class PostList(ListView):
    models = settings.OPPS_LIST_MODELS
    type = "channels"

    def get_template_names(self):
        """
        Implemented here for backwards compatibility
        """
        names = super(PostList, self).get_template_names()
        domain_folder = self.get_template_folder()
        aditional_names = [
            '{}/post_list.html'.format(domain_folder),
            'articles/post_list.html'
        ]
        if self.paginate_suffix:
            aditional_names = [
                '{}/post_list_paginated.html'.format(domain_folder),
                'articles/post_list_paginated.html'
            ]
        names = names + aditional_names
        return names

    @property
    def queryset(self):
        self.site = get_current_site(self.request).domain
        self.long_slug = self.get_long_slug()

        if not self.long_slug:
            return None

        self.set_channel_rules()

        self.articleboxes = ContainerBox.objects.filter(
            channel__long_slug=self.long_slug)

        for box in self.articleboxes:
            self.excluded_ids.update([a.pk for a in box.ordered_articles()])

        self.article = Container.objects.filter(
            site_domain=self.site,
            channel_long_slug__in=self.channel_long_slug,
            date_available__lte=timezone.now(),
            published=True,
            child_class__in=self.models,
            show_on_root_channel=True
        ).exclude(pk__in=self.excluded_ids)
        if self.limit:
            self.article = self.article[:self.limit]

        return self.article


class PostDetail(DetailView):
    model = Post
    type = 'articles'


class AlbumList(ListView):
    model = Album
    type = "channels/album"


class AlbumDetail(DetailView):
    model = Album
    type = 'articles/album'


class TagList(ListView):
    model = Container
    type = "tags"
    template_name_suffix = '_tags'
    channel_long_slug = []
    channel = None

    @property
    def queryset(self):
        self.site = get_current_site(self.request).domain
        self.long_slug = self.kwargs['tag']
        self.article = self.model.objects.filter(
            site_domain=self.site,
            tags__slug=self.long_slug,
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
