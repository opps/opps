#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from django.conf import settings
#from django.utils.importlib import import_module
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable, BaseBox


try:
    OPPS_APPS = tuple([(u"{0}.{1}".format(
        app._meta.app_label, app._meta.object_name
    ), u"{0} - {1}".format(
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
    channel = models.ForeignKey(
        'channels.Channel',
        verbose_name=_(u"Channel"),
    )

    def get_queryset(self):
        _app, _model = self.model.split('.')
        model = models.get_model(_app, _model)

        queryset = model.objects.filter(
            published=True,
            date_available__lte=timezone.now())

        try:
            if model._meta.get_field_by_name('show_on_root_channel'):
                queryset = queryset.filter(show_on_root_channel=True)
        except:
            pass  # silently pass when FieldDoesNotExists

        if self.channel and not self.channel.homepage:
            queryset = queryset.filter(channel=self.channel)
        if self.order == '-':
            queryset = queryset.order_by('-id')

        return queryset[:self.limit]

    class Meta:
        verbose_name = _(u'Queryset')
        verbose_name_plural = _(u'Querysets')


class DynamicBox(BaseBox):

    dynamicqueryset = models.ForeignKey(
        'boxes.QuerySet',
        verbose_name=_(u'Query Set')
    )

    class Meta:
        verbose_name = _(u'Dynamic Box')
        verbose_name_plural = _(u'Dynamic Boxes')
