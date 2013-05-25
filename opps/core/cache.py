#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
import md5


def _cache_key(_type, model, site, channel_long_slug):
    return md5.md5((u'{}:{}:{}:{}:{}'.format(
        _type,
        settings.OPPS_CACHE_PREFIX,
        model._meta.db_table,
        site,
        channel_long_slug)).replace(' ', '')).hexdigest()
