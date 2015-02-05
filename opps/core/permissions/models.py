# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model
from django.db import models

from opps.core.models import Date, Owned, ManyChanneling, ManySites
from opps.channels.models import Channel


User = get_user_model()
USE_DJANGO_GROUPS = issubclass(User, PermissionsMixin)


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

    @staticmethod
    def get_by_user(user):
        channels_id = set()
        channels_sites_id = set()

        # get user permissions
        sites_id = set(Permission.objects.filter(
            user=user
        ).values_list('site__id', flat=True))

        channels_qs = Permission.objects.filter(
            user=user
        ).values_list('channel__id', 'channel__site_id', 'channel_recursive')

        channels_recursive = set()
        for channel_id, site_id, channel_recursive in channels_qs:
            channels_id.add(channel_id)
            channels_sites_id.add(site_id)
            if channel_recursive:
                channels_recursive.add(channel_id)

        # get groups permissions
        if USE_DJANGO_GROUPS:
            sites_id = sites_id.union(set(PermissionGroup.objects.filter(
                group__in=user.groups.all()
            ).values_list('site__id', flat=True)))

            channels_qs = PermissionGroup.objects.filter(
                group__in=user.groups.all()
            ).values_list(
                'channel__id', 'channel__site_id', 'channel_recursive'
            )

            for channel_id, site_id, channel_recursive in channels_qs:
                channels_id.add(channel_id)
                channels_sites_id.add(site_id)
                if channel_recursive:
                    channels_recursive.add(channel_id)

        if channels_recursive:
            descendants = Channel.objects.get_queryset_descendants(
                Channel.objects.filter(
                    pk__in=channels_recursive
                )
            ).values_list('pk', flat=True)
            channels_id = channels_id.union(descendants)

        return {
            'sites_id': sites_id,
            'channels_id': channels_id,
            'channels_sites_id': channels_sites_id,
            'all_sites_id': sites_id.union(channels_sites_id)
        }


class PermissionGroup(BaseParmission):

    group = models.ForeignKey('auth.Group', verbose_name=_(u'group'))

    class Meta:
        verbose_name = _(u'Permission Group')
        verbose_name_plural = _(u'Permissions Groups')

    def __unicode__(self):
        return u'{0} em {1}'.format(self.group, self.site.all())
