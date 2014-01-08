#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from opps.core.models import NotUserPublishable


class Logging(NotUserPublishable):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        verbose_name=_(u'User')
    )
    application = models.CharField(
        _(u"Application"),
        max_length=75,
        null=True, blank=True,
        db_index=True)
    action = models.CharField(
        _(u"Action"),
        max_length=50,
        null=True, blank=True,
        db_index=True)
    text = models.TextField(
        _(u"Text"),
        null=True, blank=True,
        db_index=True)

    def save(self, *args, **kwargs):
        self.published = True
        super(Logging, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'Logging')
        verbose_name_plural = _(u'Loggings')
