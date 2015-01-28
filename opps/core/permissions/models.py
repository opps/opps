# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from opps.core.models import Publishable, ManyChanneling


class Permission(Publishable, ManyChanneling):

    @staticmethod
    def get_by_user(user):
        sites_id = []
        channels_id = []
        p = Permission.objects.filter(
            user=user,
            date_available__lte=timezone.now(),
            published=True
        ).values_list('site__id', 'channel__id')
        for s, c in p:
            sites_id.append(s)
            channels_id.append(c)

        return {'sites_id': sites_id, 'channels_id': channels_id}

    class Meta:
        verbose_name = _(u'Permission')
        verbose_name_plural = _(u'Permissions')

    def __unicode__(self):
        return u'{0} em {1}'.format(self.user, self.site)
