# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models.publishable import Publishable


class Source(Publishable):

    name = models.CharField(_(u"Name"), max_length=255)
    slug = models.SlugField(_(u"Slug"), max_length=140, unique=True,
            db_index=True)
    url = models.URLField(_(u'URL'), max_length=200, blank=True, null=True)
    feed = models.URLField(_(u'URL'), max_length=200, blank=True, null=True)


    class Meta:
        app_label = 'core'

    def __unicode__(self):
        return self.slug
