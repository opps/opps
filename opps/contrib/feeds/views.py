#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils import feedgenerator
from opps.containers.models import Container
from opps.channels.models import Channel


class ItemFeed(Feed):

    feed_type = feedgenerator.Rss201rev2Feed
    description_template = 'articles/feed_item_description.html'
    item_enclosure_length = 1
    item_enclosure_mime_type = "image/jpeg"

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_enclosure_url(self, item):
        if item.main_image:
            image_url = item.main_image.image_url()
            media_url = getattr(settings, 'MEDIA_URL', '')
            if not media_url.startswith('http'):
                image_url = "http://" + self.site.domain + image_url
            return image_url


class ContainerFeed(ItemFeed):

    link = "/rss"

    def __init__(self, child_class=False):
        self.child_class = child_class

    def __call__(self, request, *args, **kwargs):
        self.site = get_current_site(request)
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

        return container.order_by('-date_available')[:40]


class ChannelFeed(ItemFeed):

    def get_object(self, request, long_slug):
        self.site = get_current_site(request)
        return get_object_or_404(Channel,
                                 site=self.site,
                                 long_slug=long_slug)

    def link(self, obj):
        return _("{0}RSS".format(obj.get_absolute_url()))

    def title(self, obj):
        return _(u"{0}'s news on channel {1}".format(self.site.name,
                                                     obj.name))

    def description(self, obj):
        return _(u"Latest news on {0}'s channel {1}".format(self.site.name,
                                                            obj.name))

    def items(self, obj):
        return Container.objects.filter(
            site=self.site,
            channel_long_slug=obj.long_slug,
            date_available__lte=timezone.now(),
            published=True,
        ).order_by(
            '-date_available'
        ).select_related('publisher')[:40]


class ContainerAtomFeed(ContainerFeed):
    link = "/atom"
    feed_type = feedgenerator.Atom1Feed


class ChannelAtomFeed(ChannelFeed):
    feed_type = feedgenerator.Atom1Feed
