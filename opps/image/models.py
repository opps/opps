# -*- coding: utf-8 -*-
import uuid
import os
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from opps.core.models import Publishable
from opps.source.models import Source


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{0}-{1}.{2}".format(uuid.uuid4(), instance.slug, ext)
    d = datetime.now()
    folter = "images/{0}".format(d.strftime("%Y/%m/%d/"))
    return os.path.join(folter, filename)


class Image(Publishable):

    title = models.CharField(_(u"Title"), max_length=140)
    slug = models.SlugField(_(u"Slug"), max_length=150, blank=True)
    image = models.ImageField(upload_to=get_file_path)
    description = models.TextField(_(u"Description"), null=True, blank=True)

    source = models.ForeignKey(Source, null=True, blank=True)

    def __unicode__(self):
        return "{0}-{1}".format(self.id, self.slug)

    def get_absolute_url(self):
        if self.date_available <= timezone.now() and self.published:
            return self.image.url
        return u""
