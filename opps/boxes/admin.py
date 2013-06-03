#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import QuerySet
from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules


@apply_opps_rules('boxes')
class QuerySetAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    raw_id_fields = ['channel']
    exclude = ('user',)

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Rules'), {
            'fields': ('model', 'order', 'limit', 'channel')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

admin.site.register(QuerySet, QuerySetAdmin)
