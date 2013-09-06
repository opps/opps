# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable, Slugged


class Source(Publishable, Slugged):

    name = models.CharField(_(u"Name"), max_length=255)
    url = models.URLField(_(u'URL'), max_length=200, blank=True, null=True)
    feed = models.URLField(_(u'Feed URL'), max_length=200, blank=True,
                           null=True)

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')
        unique_together = ("site", "slug")

    def __unicode__(self):
        return self.name
