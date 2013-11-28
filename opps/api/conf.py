#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings

from appconf import AppConf


class OppsAPIConf(AppConf):

    NAME = getattr(settings, 'OPPS_API_NAME', u'v1')

    class Meta:
        prefix = 'opps_api'
