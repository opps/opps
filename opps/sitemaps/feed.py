#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sitemaps import GenericSitemap

from opps.article.models import Post
from opps.sitemaps.googlenews import GoogleNewsSitemap

from datetime import datetime, timedelta
from collections import OrderedDict
import isoweek


now = datetime.now()
thisweek = isoweek.Week.thisweek()

days_ago = lambda days: now - timedelta(days=days)
weeks_ago = lambda weeks: thisweek - isoweek.timedelta(weeks=weeks)


def get_sitemap(queryset, klass, date_field, location, limit, page_limit):
    if limit:
        queryset = queryset[:limit]

    if queryset.count() > 0:
        sitemap = klass({
            'queryset': queryset,
            'date_field': date_field,
            'location': location,
        })

        sitemap.limit = page_limit
        return sitemap


def process_sitemaps(sitemaps_data):
    sitemaps = OrderedDict()

    for section, data in sitemaps_data.items():
        queryset = data.get('queryset')

        if 'order_by' in data:
            queryset = queryset.order_by(data.get('order_by'))

        klass = data.get('class')

        pagination = data.get('pagination', None)
        date_field = data.get('date_field')
        location = data.get('location')
        keep = data.get('keep', 1)
        limit = data.get('limit')
        page_limit = data.get('page_limit', 50000)

        if pagination == 'weekly':
            base_queryset = queryset
            for n in range(keep):
                week = weeks_ago(n)
                sitemap_name = "%s-%s" % (section, week)

                queryset = base_queryset.filter(**{
                    "%s__gte" % date_field: week.monday(),
                    "%s__lte" % date_field: week.sunday(),
                })
                sitemap = get_sitemap(queryset, klass, date_field,
                                      location, limit, page_limit)
                if sitemap:
                    sitemaps[sitemap_name] = sitemap

        elif pagination == 'daily':
            base_queryset = queryset
            for n in range(keep):
                day = days_ago(n)
                day_before = days_ago(n - 1)
                sitemap_name = "%s-%s" % (section, day.date())

                queryset = base_queryset.filter(**{
                    "%s__gt" % date_field: day.date(),
                    "%s__lt" % date_field: day_before.date(),
                })
                sitemap = get_sitemap(queryset, klass, date_field,
                                      location, limit, page_limit)
                if sitemap:
                    sitemaps[sitemap_name] = sitemap

        else:
            sitemap = get_sitemap(queryset, klass, date_field,
                                  location, limit, page_limit)
            if sitemap:
                sitemaps[section] = sitemap

    return sitemaps

base_post_query = Post.objects.filter(published=True, date_available__lte=now)

sitemaps = {
    'post': {
        'class': GenericSitemap,
        'queryset': Post.objects.all(),
        'date_field': 'date_available',
        'order_by': '-date_available',
        'page_limit': 1000,
    },
    'googlenews': {
        'class': GoogleNewsSitemap,
        'queryset': Post.objects.all(),
        'date_field': 'date_available',
        'order_by': '-date_available',
        'limit': 1000,
    },
}

sitemaps = process_sitemaps(sitemaps)
