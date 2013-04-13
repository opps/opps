#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import get_current_site

from opps.articles.models import Article


class ArticleFeed(Feed):

    link = "/RSS"

    def __call__(self, request, *args, **kwargs):
        self.site = get_current_site(request)
        return super(ArticleFeed, self).__call__(request, *args, **kwargs)

    def title(self):
        return "{0}'s news".format(self.site.name)

    def description(self):
        return "Latest news on {0}'s".format(self.site.name)

    def items(self):
        return Article.objects.filter(site=self.site).order_by(
            '-date_available')[:40]
