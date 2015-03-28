# -*- coding: utf-8 -*-
from grappelli.views.related import AutocompleteLookup

from django.db.models import Q
from django.conf import settings
from django.contrib.sites.models import Site

from opps.core.models import Publisher, Channeling
from opps.channels.models import Channel

from .models import Permission


FALLBACK_ON_CHANNEL = getattr(settings, 'OPPS_PERMISSION_FALLBACK_ON_CHANNEL',
                              False)


class OppsAutocompleteLookup(AutocompleteLookup):

    def get_queryset(self):
        qs = super(OppsAutocompleteLookup, self).get_queryset()

        if (not settings.OPPS_MULTISITE_ADMIN or
                self.request.user.is_superuser):
            return qs

        permissions = Permission.get_by_user(self.request.user)
        filters = Q()

        if self.model == Channel:
            if FALLBACK_ON_CHANNEL:
                site_master = Site.objects.order_by('id')[0]
                permissions['sites_id'].add(site_master.pk)

            filters |= (Q(id__in=permissions['channels_id']) |
                        Q(site_id__in=permissions['sites_id']))
        elif self.model == Site:
            filters |= Q(id__in=permissions['all_sites_id'])
        else:
            if issubclass(self.model, Channeling):
                filters |= Q(channel_id__in=permissions['channels_id'])

            if issubclass(self.model, Publisher):
                filters |= Q(site_iid__in=permissions['sites_id'])

        return qs.filter(filters)
