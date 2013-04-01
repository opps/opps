# -*- coding: utf-8 -*-
from django.contrib.sitemaps import GenericSitemap as DjangoGenericSitemap
from django.contrib.sitemaps import Sitemap as DjangoSitemap
from django.utils import timezone

from opps.articles.models import Article


def InfoDisct(googlenews=False):
    article = Article.objects.filter(date_available__lte=timezone.now(),
                                     published=True)
    if googlenews:
        article = article[:1000]
    return {
        'queryset': article,
        'date_field': 'date_available',
    }


class BaseSitemap(DjangoSitemap):
    priority = 0.6

    def items(self):
        return Article.objects.filter(date_available__lte=timezone.now(),
                                      published=True)

    def lastmod(self, obj):
        return obj.date_available


class GenericSitemap(DjangoGenericSitemap):
    limit = 1000
    priority = 0.6
