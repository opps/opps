# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models.publishable import Publishable
from opps.core.models import Source



class Image(Publishable):

    title = models.CharField(_(u"Title"), max_length=140)
    slug = models.SlugField(_(u"Slug"), max_length=150, blank=True)
    image = models.ImageField(upload_to="uploads/")
    description = models.CharField(_(u"Description"), max_length=255,
            null=True, blank=True)

    source = models.ForeignKey(Source, null=True, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'core'
