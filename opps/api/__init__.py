#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tastypie.constants import ALL


class MetaBase:
    allowed_methods = ['get']
    filtering = {
        'site_domain': ALL,
        'channel_long_slug': ALL,
        'child_class': ALL,
        'tags': ALL,
    }
