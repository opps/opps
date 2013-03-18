# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable
from opps.source.models import Source


class Image(Publishable):

    title = models.CharField(_(u"Title"), max_length=140)
    slug = models.SlugField(_(u"Slug"), max_length=150, blank=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(_(u"Description"), null=True, blank=True)

    source = models.ForeignKey(Source, null=True, blank=True)

    def __unicode__(self):
        return "{0}-{1}".format(self.id, self.slug)
