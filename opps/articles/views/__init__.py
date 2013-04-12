#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage
from django.contrib.sites.models import get_current_site
from django.utils import timezone
from django.http import Http404

from haystack.views import SearchView

from opps.articles.models import Post, Album, Article
from opps.articles.views.generic import OppsDetail, OppsList


class PostList(OppsList):
    model = Post
    type = "channels"


class PostDetail(OppsDetail):
    model = Post
    type = 'articles'


class AlbumList(OppsList):
    model = Album
    type = "channels/album"


class AlbumDetail(OppsDetail):
    model = Album
    type = 'articles/album'


class TagList(OppsList):
    model = Article
    type = "tags"
    template_name_suffix = '_tags'

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        self.long_slug = self.kwargs['tag']
        self.article = self.model.objects.filter(
            site=self.site,
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
