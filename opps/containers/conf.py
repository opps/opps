#!/usr/bin/env python
# -*- coding: utf-8 -*-
from appconf import AppConf


class OppsContainerConf(AppConf):

    SITE_ID = None

    class Meta:
        prefix = 'opps_containers'
