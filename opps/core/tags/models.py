# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Date, Slugged


class Tag(Date, Slugged):
    name = models.CharField(_(u'Tag'), max_length=4000)

    __unicode__ = lambda self: self.name

    class Meta:
        verbose_name = _(u'Tag')
        verbose_name_plural = _(u'Tags')
