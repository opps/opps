# -*- coding: utf-8 -*-
from opps.core.models import Date, Owned, ManyChanneling, ManySites
from django.utils.translation import ugettext_lazy as _
from django.db import models


class BaseParmission(ManyChanneling, ManySites, Date):
    channel_recursive = models.BooleanField(
        _(u'channel recursive'),
        default=False
    )

    class Meta:
        abstract = True


class Permission(BaseParmission, Owned):

    class Meta:
        verbose_name = _(u'Permission')
        verbose_name_plural = _(u'Permissions')

    def __unicode__(self):
        return u'{0} em {1}'.format(self.user, self.site.all())


class PermissionGroup(BaseParmission):

    group = models.ForeignKey('auth.Group', verbose_name=_(u'group'))

    class Meta:
        verbose_name = _(u'Permission Group')
        verbose_name_plural = _(u'Permissions Groups')

    def __unicode__(self):
        return u'{0} em {1}'.format(self.group, self.site.all())
