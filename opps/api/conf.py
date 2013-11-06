#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings

from appconf import AppConf


class OppsAPIConf(AppConf):

    PAGINATE_BY = getattr(settings, 'OPPS_API_PAGINATE_BY', 12)

    class Meta:
        prefix = 'opps_api'
