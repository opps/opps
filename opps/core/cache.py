#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.views.decorators.cache import cache_page as django_cache_page

from hashlib import md5


def _cache_key(_type, model, site, channel_long_slug):
    return md5((u'{0}:{1}:{2}:{3}:{4}'.format(
        _type,
        settings.OPPS_CACHE_PREFIX,
        model._meta.db_table,
        site,
        channel_long_slug)).replace(' ', '')).hexdigest()


def cache_page(*dec_args, **dec_kwargs):
    cache_timeout = dec_args[0] if dec_args else settings.OPPS_CACHE_EXPIRE
    cache_alias = dec_kwargs.pop('cache', None)
    key_prefix = dec_kwargs.pop('key_prefix', '')

    def decorator(func):
        def wrapped(*func_args, **func_kwargs):
            request = func_args[0]
            cache_prefix = u'{0}-{1}-{2}'.format(
                key_prefix,
                get_current_site(request).domain,
                getattr(request, 'is_mobile', False)
            )

            do_cache = django_cache_page(
                cache_timeout,
                cache=cache_alias,
                key_prefix=cache_prefix
            )(lambda *args, **kwargs: func(*func_args, **func_kwargs))

            return do_cache(*func_args, **func_kwargs)
        return wrapped
    return decorator
