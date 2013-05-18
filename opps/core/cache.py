#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from base64 import b64encode


def _cache_key(_type, model, site, channel_long_slug):
    return b64encode((u'{}:{}:{}:{}:{}'.format(
        _type,
        settings.OPPS_CACHE_PREFIX,
        model._meta.db_table,
        site,
        channel_long_slug)).replace(' ', ''))
