#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


from opps.core.models import Publishable, Slugged


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = u"{0}-{1}.{2}".format(random.getrandbits(32),
                                     instance.slug[:100], ext)
    d = datetime.now()
    folder = "archives/{0}".format(d.strftime("%Y/%m/%d/"))
    return os.path.join(folder, filename)


class Archive(Publishable, Slugged):

    title = models.CharField(_(u"Title"), max_length=140, db_index=True)
    archive = models.FileField(upload_to=get_file_path, max_length=255)
    description = models.TextField(_(u"Description"), null=True, blank=True)

    source = models.ForeignKey('sources.Source', null=True, blank=True)

    class Meta:
        verbose_name = _('Archive')
        verbose_name_plural = _('Archives')
        unique_together = ['site', 'slug']
        abstract = True

    def __unicode__(self):
        return u"{}-{}".format(self.site, self.slug)

    def get_absolute_url(self):
        if self.date_available <= timezone.now() and self.published:
            return self.archive.url
        return u""
