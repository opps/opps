# -*- coding: utf-8 -*-
import warnings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple

from opps.core.permissions.admin import AdminViewPermission as NewAVP
from opps.core.permissions.admin import PermissionAdmin as NewSPA

from .models import SitePermission


warn = "opps.contrib.multisite will be removed, must use opps.core.permission"


class AdminViewPermission(NewAVP):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        warnings.warn(warn, DeprecationWarning)
        return super(AdminViewPermission, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def queryset(self, request):
        warnings.warn(warn, DeprecationWarning)
        return super(AdminViewPermission, self).queryset(request)

    def get_form(self, request, obj=None, **kwargs):
        warnings.warn(warn, DeprecationWarning)
        return super(AdminViewPermission, self).get_form(
            request, obj=None, **kwargs)


class SitePermissionAdmin(NewSPA):
    raw_id_fields = ('user',)
    exclude = ('site_iid', 'mirror_site', 'site_domain')
