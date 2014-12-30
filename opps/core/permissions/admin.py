# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple

from opps.channels.models import Channel

from .models import Permission


class AdminViewPermission(admin.ModelAdmin):

    @property
    def site_lookup(self):
        return 'site_iid__in'

    def permission_in(self, user):
        sites_id = []
        channels_id = []
        p = Permission.objects.filter(
            user=user,
            date_available__lte=timezone.now(),
            published=True
        ).values_list('site__id', 'channel__id')
        for s,c in p:
            sites_id.append(s)
            channels_id.append(c)

        return {'sites_id': set(sites_id), 'channels_id': channels_id}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if settings.OPPS_MULTISITE_ADMIN and not request.user.is_superuser:
            obj = self.permission_in(request.user)

            if db_field.name in ['site']:
                kwargs['queryset'] = Site.objects.filter(
                    id__in=obj.get('sites_id', []))

            if db_field.name in ['channel']:
                kwargs['queryset'] = Channel.objects.filter(
                    id__in=obj.get('channels_id', []))

        return super(AdminViewPermission, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def queryset(self, request):
        qs = super(AdminViewPermission, self).queryset(request)
        if not settings.OPPS_MULTISITE_ADMIN or request.user.is_superuser:
            return qs

        obj = self.permission_in(request.user)

        if self.__class__.__name__ == 'ChannelAdmin':
            return qs.filter(**{
                'site__id__in': obj.get('sites_id', []),
                'id__in': obj.get('channels_id', [])})
        return qs.filter(**{
            'site_iid__in': obj.get('sites_id', []),
            'channel__id__in': obj.get('channels_id', [])})

    def get_form(self, request, obj=None, **kwargs):
        form = super(AdminViewPermission, self).get_form(
            request, obj, **kwargs)
        obj = self.permission_in(request.user)

        try:
            attrs_mirror = {}
            if settings.OPPS_MULTISITE_ADMIN and not request.user.is_superuser:
                qs_mirror = form.base_fields['mirror_site'].queryset
                form.base_fields['mirror_site'].queryset = qs_mirror.filter(
                    id__in=obj.get('sites_id', []))
                attrs_mirror = {'disabled': 'disabled'}

            form.base_fields['mirror_site'].widget = FilteredSelectMultiple(
                _("Mirror site"), is_stacked=False, attrs=attrs_mirror)
        except:
            pass

        try:
            if settings.OPPS_MULTISITE_ADMIN and not request.user.is_superuser:
                qs_channel = form.base_fields['channel'].queryset
                form.base_fields['channel'].queryset = qs_channel.filter(
                    id__in=obj.get('channels_id', []))
        except:
            pass

        return form


class PermissionAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    filter_horizontal = ('channel',)
    exclude = ('site_iid', 'mirror_site', 'site_domain')


admin.site.register(Permission, PermissionAdmin)
