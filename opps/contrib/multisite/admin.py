#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils import timezone

from .models import SitePermission


class AdminViewPermission(admin.ModelAdmin):

    def queryset(self, request):
        queryset = super(AdminViewPermission, self).queryset(request)
        try:
            sitepermission = SitePermission.objects.get(
                user=request.user,
                date_available__lte=timezone.now(),
                published=True)
            return queryset.filter(site_iid=sitepermission.site_iid)
        except SitePermission.DoesNotExist:
            pass
        return queryset

    def get_form(self, request, obj=None, **kwargs):
        form = super(AdminViewPermission, self).get_form(request, obj,
                                                         **kwargs)
        try:
            sitepermission = SitePermission.objects.get(
                user=request.user,
                date_available__lte=timezone.now(),
                published=True)
            form.base_fields['site'].initial = sitepermission.site
            form.base_fields['site'].choices = ((sitepermission.site.id,
                                                 sitepermission.site.domain),)
        except SitePermission.DoesNotExist:
            pass

        return form


admin.site.register(SitePermission)
