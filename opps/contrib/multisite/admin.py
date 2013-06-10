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


admin.site.register(SitePermission)
