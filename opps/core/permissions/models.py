# -*- coding: utf-8 -*-
from opps.core.models import Publishable, ManyChanneling
from django.utils.translation import ugettext_lazy as _


class Permission(Publishable, ManyChanneling):
    class Meta:
        verbose_name = _(u'Permission')
        verbose_name_plural = _(u'Permissions')

    def __unicode__(self):
        return u'{0} em {1}'.format(self.user, self.site)
