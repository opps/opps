#!/usr/bin/env python
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from opps.core.models.date import Date

from datetime import datetime



class PublishedMnager(models.Manager):
    def all_published(self):
        return super(PublisherMnager, self).get_query_set().filter(
                date_available__lte=datetime.now(), published=True)


class Publishable(Date):

    user = models.ForeignKey(User)
    site = models.ForeignKey(Site, default=0)
    date_available = models.DateTimeField(_(u"Date available"),
            default=datetime.now, null=True)
    publisher = models.BooleanField(_(u"Publisher"), default=False)

    objects = PublishedMnager()

    class Meta:
        abstract = True

    def is_published(self):
        return self.published and \
                self.date_available.replace(tzinfo=None) <= datetime.now()
