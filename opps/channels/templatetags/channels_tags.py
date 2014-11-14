# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.cache import cache

from opps.channels.models import Channel


register = template.Library()


@register.assignment_tag
def get_channel(slug):
    """
        Usage:

        {% get_channel "videos" %}
    """
    try:
        return Channel.objects.get(site=settings.SITE_ID, slug=slug,
                                   published=True)
    except Channel.DoesNotExist:
        return Channel.objects.none()


@register.assignment_tag
def get_channels_by(**filters):
    """Return a list of channels filtered by given args"""
    filters['site'] = filters.get('site', settings.SITE_ID)
    filters['published'] = filters.get('published', True)

    if not filters['site']:
        del filters['site']

    cache_key = u'getchannelsby-{0}'.format(hash(frozenset(filters.items())))
    cache_timeout = getattr(settings, 'OPPS_CACHE_EXPIRE')

    if cache_timeout and cache.get(cache_key):
        return cache.get(cache_key)

    channels = Channel.objects.filter(**filters)

    if cache_timeout:
        cache.set(cache_key, channels, cache_timeout)

    return channels
