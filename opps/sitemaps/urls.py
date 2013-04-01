#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.sitemaps import views as sitemap_views

from opps.sitemaps.sitemaps import GenericSitemap, InfoDisct


sitemaps = {
    'articles': GenericSitemap(InfoDisct(), priority=0.6),
}

sitemaps_googlenews = {
    'articles': GenericSitemap(InfoDisct(True), priority=0.6),
}

urlpatterns = patterns(
    '',
    url(r'^\.xml$', sitemap_views.index,
        {'sitemaps': sitemaps}),
    url(r'^-googlenews\.xml$', sitemap_views.sitemap,
        {'sitemaps': sitemaps_googlenews,
         'template_name': 'sitemap_googlenews.xml'}),
    url(r'^-(?P<section>.+)\.xml$', sitemap_views.sitemap,
        {'sitemaps': sitemaps}),

)
