#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from django.conf import settings
#from django.utils.importlib import import_module
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable, BaseBox


try:
    OPPS_APPS = tuple([(u"{0}.{1}".format(
        app._meta.app_label, app._meta.object_name), u"{0} - {1}".format(
            app._meta.app_label, app._meta.object_name))
        for app in models.get_models() if 'opps.' in app.__module__])
except ImportError:
    OPPS_APPS = tuple([])


class QuerySet(Publishable):
    name = models.CharField(_(u"Dynamic queryset name"), max_length=140)
    slug = models.SlugField(
        _(u"Slug"),
        db_index=True,
        max_length=150,
        unique=True,
    )

    model = models.CharField(_(u'Model'), max_length=150, choices=OPPS_APPS)
    limit = models.PositiveIntegerField(_(u'Limit'), default=7)
    order = models.CharField(_('Order'), max_length=1, choices=(
        ('-', 'DESC'), ('+', 'ASC')))


class DynamicBox(BaseBox):

    dynamicqueryset = models.ForeignKey(
        'boxes.QuerySet',
        verbose_name=_(u'Query Set')
    )
