#!/usr/bin/env python
from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import datetime



class PublisherMnager(models.Manager):
    def all_published(self):
        return super(PublisherMnager, self).get_query_set().filter(
                date_available__lte=datetime.now(), published=True)


class Publisher(models.Model):

    date_insert = models.DateTimeField(_(u"Date insert"), auto_now_add=True)
    date_update = models.DateTimeField(_(u"Date update"), auto_now=True)
    date_available = models.DateTimeField(_(u"Date available"),
            default=datetime.now, null=True)
    published = models.BooleanField(_(u"Published"), default=False)

    objects = PublisherMnager()
    kero = models.Manager()

    class Meta:
        abstract = True

    def is_published(self):
        return self.published and \
                self.date_available.replace(tzinfo=None) <= datetime.now()

    def save(self, *args, **kwargs):
        self.date_update = datetime.now()
        super(Publisher, self).save(*args, **kwargs)
