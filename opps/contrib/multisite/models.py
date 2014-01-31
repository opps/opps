#!/usr/bin/env python
# -*- coding: utf-8 -*-
from opps.core.models import Publishable
from django.utils.translation import ugettext_lazy as _


class SitePermission(Publishable):
    """
    Join user in site
    """
    class Meta:
        verbose_name = _(u'Site Permission')
        verbose_name_plural = _(u'Site Permissions')

    def __unicode__(self):
        return u'{} em {}'.format(self.user, self.site)
