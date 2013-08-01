#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings

from appconf import AppConf


class OppsDataBaseConf(AppConf):

    HOST = getattr(settings, 'OPPS_DB_HOSR', None)
    USER = getattr(settings, 'OPPS_DB_USER', None)
    PASSWORD = getattr(settings, 'OPPS_DB_PASSWORD', None)
    PORT = getattr(settings, 'OPPS_DB_PORT', None)
    NAME = getattr(settings, 'OPPS_DB_NAME', 'opps_db')
    ENGINE = getattr(settings, 'OPPS_DB_ENGINE', 'opps.db.')
    OPTION = getattr(settings, 'OPPS_BD_OPTION', None)

    class Meta:
        prefix = 'opps_db'
