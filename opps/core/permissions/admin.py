# -*- coding: utf-8 -*-
import warnings
from django.contrib import admin
from django.db.models import Q
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple

from opps.channels.models import Channel
from opps.core.models import Channeling, Publisher

from .models import Permission, PermissionGroup


FALLBACK_ON_CHANNEL = getattr(settings, 'OPPS_PERMISSION_FALLBACK_ON_CHANNEL',
                              False)


class AdminViewPermission(admin.ModelAdmin):

    _site_master = None

    def _get_site_master(self):
        if self._site_master:
            return self._site_master

        self._site_master = Site.objects.order_by('id')[0]
        return self._site_master

    @property
    def site_lookup(self):
        warnings.warn("site_lookup will be removed!", DeprecationWarning)
        return 'site_iid__in'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if settings.OPPS_MULTISITE_ADMIN and not request.user.is_superuser:
            obj = Permission.get_by_user(request.user)

            if db_field.name in ['site']:
                kwargs['queryset'] = Site.objects.filter(
                    id__in=obj['all_sites_id']
                )

            if db_field.name in ['channel']:
                if FALLBACK_ON_CHANNEL:
                    obj['sites_id'].add(self._get_site_master().pk)

                kwargs['queryset'] = Channel.objects.filter(
                    Q(id__in=obj['channels_id']) |
                    Q(site_id__in=obj['sites_id'])
                )

        return super(AdminViewPermission, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def queryset(self, request):
        qs = super(AdminViewPermission, self).queryset(request)
        if not settings.OPPS_MULTISITE_ADMIN or request.user.is_superuser:
            return qs

        obj = Permission.get_by_user(request.user)

        if self.__class__.__name__ == 'ChannelAdmin':
            if FALLBACK_ON_CHANNEL:
                obj['sites_id'].add(self._get_site_master().pk)

            return qs.filter(
                Q(site_id__in=obj['sites_id']) |
                Q(id__in=obj['channels_id'])
            )

        filters = Q()

        if issubclass(qs.model, Publisher):
            filters |= Q(site_iid__in=obj['sites_id'])

        if issubclass(qs.model, Channeling):
            filters |= Q(channel_id__in=obj['channels_id'])

        return qs.filter(filters)

    def get_form(self, request, obj=None, **kwargs):
        form = super(AdminViewPermission, self).get_form(
            request, obj, **kwargs)
        obj = Permission.get_by_user(request.user)

        try:
            attrs_mirror = {}
            if settings.OPPS_MULTISITE_ADMIN and not request.user.is_superuser:
                qs_mirror = form.base_fields['mirror_site'].queryset
                form.base_fields['mirror_site'].queryset = qs_mirror.filter(
                    id__in=obj['all_sites_id']
                )
                attrs_mirror = {'disabled': 'disabled'}

            form.base_fields['mirror_site'].widget = FilteredSelectMultiple(
                _("Mirror site"), is_stacked=False, attrs=attrs_mirror)
        except:
            pass

        try:
            if settings.OPPS_MULTISITE_ADMIN and not request.user.is_superuser:
                if FALLBACK_ON_CHANNEL:
                    obj['sites_id'].add(self._get_site_master().pk)

                qs_channel = form.base_fields['channel'].queryset
                form.base_fields['channel'].queryset = qs_channel.filter(
                    Q(site_id__in=obj['sites_id']) |
                    Q(id__in=obj['channels_id'])
                )
        except:
            pass

        return form


class PermissionAdmin(admin.ModelAdmin):
    fields = ('user', 'channel', 'channel_recursive', 'site')
    raw_id_fields = ('user',)
    filter_horizontal = ('channel',)

admin.site.register(Permission, PermissionAdmin)


class PermissionGroupAdmin(admin.ModelAdmin):
    fields = ('group', 'channel', 'channel_recursive', 'site')
    raw_id_fields = ('group',)
    filter_horizontal = ('channel',)

admin.site.register(PermissionGroup, PermissionGroupAdmin)
