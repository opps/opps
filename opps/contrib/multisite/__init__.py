#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from appconf import AppConf


trans_app_label = _('Multisite')


class OppsMultiSiteConf(AppConf):
    ADMIN = False

    class Meta:
        prefix = 'opps_multisite'
