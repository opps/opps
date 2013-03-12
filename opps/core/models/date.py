#!/usr/bin/env python
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Date(models.Model):

    date_insert = models.DateTimeField(_(u"Date insert"), auto_now_add=True)
    date_update = models.DateTimeField(_(u"Date update"), auto_now=True)

    class Meta:
        abstract = True
