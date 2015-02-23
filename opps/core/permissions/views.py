# -*- coding: utf-8 -*-
from grappelli.views.related import AutocompleteLookup

from django.db.models import Q
from django.conf import settings

from opps.core.models import Publisher, Channeling
from opps.channels.models import Channel

from .models import Permission


class OppsAutocompleteLookup(AutocompleteLookup):

    def get_queryset(self):
        qs = super(OppsAutocompleteLookup, self).get_queryset()

        if (not settings.OPPS_MULTISITE_ADMIN or
                self.request.user.is_superuser):
            return qs

        permissions = Permission.get_by_user(self.request.user)
        filters = Q()

        if self.model == Channel:
            filters |= (Q(id__in=permissions['channels_id']) |
                        Q(site_id__in=permissions['sites_id']))
        else:
            if issubclass(self.model, Channeling):
                filters |= Q(channel_id__in=permissions['channels_id'])

            if issubclass(self.model, Publisher):
                filters |= Q(site_iid__in=permissions['all_sites_id'])

        return qs.filter(filters)
