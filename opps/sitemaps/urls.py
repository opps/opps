#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.sitemaps import views as sitemap_views

from opps.core.cache import cache_page

from opps.sitemaps.sitemaps import GenericSitemap, InfoDict
from opps.sitemaps.views import sitemap

sitemaps = {
    'containers': GenericSitemap(InfoDict(), priority=0.6),
}

sitemaps_googlenews = {
    'containers': GenericSitemap(InfoDict(True), priority=0.6),
}

urlpatterns = patterns(
    '',
    url(r'^\.xml$', cache_page(86400)(sitemap_views.index),
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'},),
    url(r'^-googlenews\.xml$',
        cache_page(86400)(sitemap),
        {'sitemaps': sitemaps_googlenews,
         'template_name': 'sitemap_googlenews.xml'}),
    url(r'^-(?P<section>.+)\.xml$',
        cache_page(86400)(sitemap_views.sitemap),
        {'sitemaps': sitemaps}, name='sitemaps'),
)
