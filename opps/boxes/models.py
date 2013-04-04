#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from django.conf import settings
#from django.utils.importlib import import_module
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable, BaseBox


"""
from django.db.models import get_model
model = get_model('myapp', 'modelA')
model.objects.filter(**kwargs)

(Pdb)  models.get_models()[15]._meta.local_fields[0].verbose_name
u'ID'
(Pdb)  models.get_models()[15]._meta.local_fields[0].name
u'id'
"""

try:
    OPPS_APPS = tuple([(app._meta.app_label, u"{0} - {1}".format(
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


class DynamicBox(BaseBox):

    dynamicqueryset = models.ForeignKey(
        'boxes.QuerySet',
        verbose_name=_(u'Query Set')
    )
