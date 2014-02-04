#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import SitePermission


class AdminViewPermission(admin.ModelAdmin):

    site_lookup = 'site_iid__in'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if settings.OPPS_MULTISITE_ADMIN and not request.user.is_superuser:
            sites_id = SitePermission.objects.filter(
                user=request.user,
                date_available__lte=timezone.now(),
                published=True
            ).values_list('site__id', flat=True)

            if db_field.name in ['site']:
                kwargs['queryset'] = Site.objects.filter(id__in=sites_id)

        result = super(AdminViewPermission, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

        return result

    def queryset(self, request):
        qs = super(AdminViewPermission, self).queryset(request)
        if not settings.OPPS_MULTISITE_ADMIN or request.user.is_superuser:
            return qs

        sites_id = SitePermission.objects.filter(
            user=request.user,
            date_available__lte=timezone.now(),
            published=True
        ).values_list('site__id', flat=True)

        return qs.filter(**{self.site_lookup: sites_id})

    def get_form(self, request, obj=None, **kwargs):

        form = super(
            AdminViewPermission, self
        ).get_form(request, obj, **kwargs)

        sites_id = SitePermission.objects.filter(
            user=request.user,
            date_available__lte=timezone.now(),
            published=True
        ).values_list('site__id', flat=True)

        try:
            attrs = {}
            if settings.OPPS_MULTISITE_ADMIN and not request.user.is_superuser:
                qs = form.base_fields['mirror_site'].queryset
                form.base_fields['mirror_site'].queryset = qs.filter(
                    id__in=sites_id
                )
                attrs = {'disabled': 'disabled'}
            form.base_fields['mirror_site'].widget = FilteredSelectMultiple(
                _("Mirror site"), is_stacked=False, attrs=attrs
            )
        except:
            pass

        return form


class SitePermissionAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    exclude = ('site_iid', 'mirror_site', 'site_domain')


admin.site.register(SitePermission, SitePermissionAdmin)
