#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sitemaps import GenericSitemap as DjangoGenericSitemap
from django.contrib.sitemaps import Sitemap as DjangoSitemap
from django.utils import timezone

from opps.containers.models import Container


def InfoDict(googlenews=False):
    containers = Container.objects.filter(date_available__lte=timezone.now(),
                                          published=True)
    if googlenews:
        containers = containers[:1000]
    return {
        'queryset': containers,
        'date_field': 'date_available',
    }


class BaseSitemap(DjangoSitemap):
    priority = 0.6

    def items(self):
        return Container.objects.filter(date_available__lte=timezone.now(),
                                        published=True)

    def lastmod(self, obj):
        return obj.date_available


class GenericSitemap(DjangoGenericSitemap):
    limit = 1000
    priority = 0.6
