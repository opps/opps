#!/usr/bin/env python
from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import datetime


class Date(models.Model):

    date_insert = models.DateTimeField(_(u"Date insert"), auto_now_add=True)
    date_update = models.DateTimeField(_(u"Date update"), auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.date_update = datetime.now()
        super(Date, self).save(*args, **kwargs)
