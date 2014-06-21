#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils import feedgenerator
from opps.containers.models import Container
from opps.channels.models import Channel


OPPS_FEED_FILTER_DEFAULT = getattr(settings, 'OPPS_FEED_FILTER_DEFAULT', {})
OPPS_FEED_EXCLUDE_DEFAULT = getattr(settings, 'OPPS_FEED_EXCLUDE_DEFAULT', {})


class ItemFeed(Feed):

    feed_type = feedgenerator.Rss201rev2Feed
    description_template = 'articles/feed_item_description.html'
    item_enclosure_length = 1
    item_enclosure_mime_type = "image/jpeg"

    def item_categories(self, obj):
        cats = []
        if obj.channel:
            cats.append(obj.channel.name)
        if getattr(obj, 'tags', None) is not None:
            cats.extend(obj.get_tags() or [])
        return cats

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_available

    def item_updateddate(self, item):
        return item.date_update

    def item_link(self, item):
        return item.get_absolute_url()

    def item_enclosure_url(self, item):
        if item.main_image:
            if item.main_image.archive:
                i_url = item.main_image.archive.url
            elif item.main_image.archive_link:
                i_url = item.main_image.archive_link
            else:
                i_url = item.main_image.image_url()

            m_url = getattr(settings, 'MEDIA_URL', '')
            if not m_url.startswith('http') and not i_url.startswith('http'):
                i_url = "http://" + self.site.domain + i_url
            return i_url

    def build_filters(self):
        if not hasattr(self, 'request'):
            return {}

        default = {
            "filter": OPPS_FEED_FILTER_DEFAULT,
            "exclude": OPPS_FEED_EXCLUDE_DEFAULT, }

        data = {"filter": {}, "exclude": {}, }

        r_data = self.request.GET.dict()

        for k, v in r_data.items():
            if k.startswith(('filter', 'exclude')):
                v = json.loads(v)
                for lookup, value in v.items():
                    if lookup.endswith('__in'):
                        v[lookup] = value.split(',')
                data[k].update(v)

        # merges defaults with request.GET data.
        for k, v in data.items():
            data[k] = dict(default[k].items() + v.items())

        return data


class ContainerFeed(ItemFeed):

    link = "/rss"

    def __init__(self, child_class=False):
        self.child_class = child_class

    def __call__(self, request, *args, **kwargs):
        self.site = get_current_site(request)
        self.request = request
        return super(ContainerFeed, self).__call__(request, *args, **kwargs)

    def title(self):
        return _("{0}'s news".format(self.site.name))

    def description(self):
        return _("Latest news on {0}'s".format(self.site.name))

    def items(self):
        container = Container.objects.filter(
            site=self.site,
            date_available__lte=timezone.now(),
            published=True,
            channel__include_in_main_rss=True,
            channel__published=True
        )

        if self.child_class:
            container = container.filter(child_class=self.child_class)

        container = container.exclude(child_class__in=['Mirror', 'Entry'])

        return container.order_by('-date_available')[:40]


class ChannelFeed(ItemFeed):
    """
    Items can be filtered using "filter" and "exclude" querystring args.
    examples:

    - get only entries with images
    rss?filter={"main_image__isnull": false}

    - exclude specific child_class
    rss?exclude={"child_class__in": "Album,Poll"}

    The format is json
    """

    def get_object(self, request, long_slug):
        self.site = get_current_site(request)
        self.request = request
        channel = get_object_or_404(Channel,
                                    site=self.site,
                                    long_slug=long_slug)
        self.channel_descendants = channel.get_descendants(include_self=True)
        return channel

    def link(self, obj):
        return _("{0}RSS".format(obj.get_absolute_url()))

    def title(self, obj):
        return _(u"{0}'s news on channel {1}".format(self.site.name,
                                                     obj.name))

    def description(self, obj):
        return _(u"Latest news on {0}'s channel {1}".format(self.site.name,
                                                            obj.name))

    def items(self, obj):
        filters = self.build_filters().get('filter', {})
        excludes = self.build_filters().get('exclude', {})

        channel_long_slugs = [
            children.long_slug for children in
            self.channel_descendants
        ]

        qs = Container.objects.filter(
            site=self.site,
            channel_long_slug__in=channel_long_slugs,
            date_available__lte=timezone.now(),
            published=True,
            **filters
        ).exclude(
            child_class__in=['Mirror', 'Entry'],
        ).exclude(
            **excludes
        )

        qs = qs.order_by(
            '-date_available'
        ).select_related('publisher')[:40]

        return qs


class ContainerAtomFeed(ContainerFeed):
    link = "/atom"
    feed_type = feedgenerator.Atom1Feed


class ChannelAtomFeed(ChannelFeed):
    feed_type = feedgenerator.Atom1Feed
