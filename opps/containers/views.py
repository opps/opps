#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import Http404

from haystack.views import SearchView

from opps.containers.models import Container
from opps.channels.models import Channel
from opps.views.generic.list import ListView
from opps.views.generic.detail import DetailView


class ContainerList(ListView):
    model = Container


class ContainerDetail(DetailView):
    model = Container


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


class ItemFeed(Feed):

    description_template = 'articles/feed_item_description.html'

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()


class ContainerFeed(ItemFeed):

    link = "/rss"

    def __call__(self, request, *args, **kwargs):
        self.site = get_current_site(request)
        return super(ContainerFeed, self).__call__(request, *args, **kwargs)

    def title(self):
        return "{0}'s news".format(self.site.name)

    def description(self):
        return "Latest news on {0}'s".format(self.site.name)

    def items(self):
        return Container.objects.filter(
            site=self.site,
            date_available__lte=timezone.now(),
            published=True,
            channel__include_in_main_rss=True,
            channel__published=True
        ).order_by(
            '-date_available'
        )[:40]


class ChannelFeed(ItemFeed):

    def get_object(self, request, long_slug):
        self.site = get_current_site(request)
        return get_object_or_404(Channel,
                                 site=self.site,
                                 long_slug=long_slug)

    def link(self, obj):
        return "{0}RSS".format(obj.get_absolute_url())

    def title(self, obj):
        return u"{0}'s news on channel {1}".format(self.site.name, obj.name)

    def description(self, obj):
        return u"Latest news on {0}'s channel {1}".format(self.site.name,
                                                          obj.name)

    def items(self, obj):
        return Container.objects.filter(
            site=self.site,
            channel_long_slug=obj.long_slug,
            date_available__lte=timezone.now(),
            published=True,
        ).order_by(
            '-date_available'
        ).select_related('publisher')[:40]
