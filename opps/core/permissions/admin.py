# -*- coding: utf-8 -*-
import warnings
from django.contrib import admin
from django.db.models import Q
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple

from opps.channels.models import Channel

from .models import Permission, PermissionGroup

User = get_user_model()
USE_DJANGO_GROUPS = issubclass(User, PermissionsMixin)


class AdminViewPermission(admin.ModelAdmin):

    @property
    def site_lookup(self):
        warnings.warn("site_lookup will be removed!", DeprecationWarning)
        return 'site_iid__in'

    def permission_in(self, user):
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if settings.OPPS_MULTISITE_ADMIN and not request.user.is_superuser:
            obj = self.permission_in(request.user)

            if db_field.name in ['site']:
                kwargs['queryset'] = Site.objects.filter(
                    id__in=obj.get('all_sites_id', [])
                )

            if db_field.name in ['channel']:
                kwargs['queryset'] = Channel.objects.filter(
                    Q(id__in=obj.get('channels_id', [])) |
                    Q(site_id__in=obj.get('sites_id', []))
                )

        return super(AdminViewPermission, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def queryset(self, request):
        qs = super(AdminViewPermission, self).queryset(request)
        if not settings.OPPS_MULTISITE_ADMIN or request.user.is_superuser:
            return qs

        obj = self.permission_in(request.user)

        if self.__class__.__name__ == 'ChannelAdmin':
            return qs.filter(
                Q(site_id__in=obj.get('sites_id', [])) |
                Q(id__in=obj.get('channels_id', []))
            )

        return qs.filter(
            Q(site_iid__in=obj.get('sites_id', [])) |
            Q(channel_id__in=obj.get('channels_id', []))
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super(AdminViewPermission, self).get_form(
            request, obj, **kwargs)
        obj = self.permission_in(request.user)

        try:
            attrs_mirror = {}
            if settings.OPPS_MULTISITE_ADMIN and not request.user.is_superuser:
                qs_mirror = form.base_fields['mirror_site'].queryset
                form.base_fields['mirror_site'].queryset = qs_mirror.filter(
                    id__in=obj.get('all_sites_id', [])
                )
                attrs_mirror = {'disabled': 'disabled'}

            form.base_fields['mirror_site'].widget = FilteredSelectMultiple(
                _("Mirror site"), is_stacked=False, attrs=attrs_mirror)
        except:
            pass

        try:
            if settings.OPPS_MULTISITE_ADMIN and not request.user.is_superuser:
                qs_channel = form.base_fields['channel'].queryset
                form.base_fields['channel'].queryset = qs_channel.filter(
                    Q(site_id__in=obj.get('sites_id', [])) |
                    Q(id__in=obj.get('channels_id', []))
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
