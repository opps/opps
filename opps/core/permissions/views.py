# -*- coding: utf-8 -*-
from grappelli.views.related import AutocompleteLookup
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

        if self.model == Channel:
            qs = qs.filter(id__in=permissions.get('channels_id', []))
        elif issubclass(self.model, Channeling):
            qs = qs.filter(channel__id__in=permissions.get('channels_id', []))

        if issubclass(self.model, Publisher):
            qs = qs.filter(site_iid__in=permissions.get('sites_id', []))

        return qs
