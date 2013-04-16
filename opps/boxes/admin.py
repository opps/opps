#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import QuerySet, DynamicBox
from opps.core.admin import PublishableAdmin


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


class DynamicBoxAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    exclude = ('user',)
    raw_id_fields = ['channel', 'article', 'dynamicqueryset']
    search_fields = ['name', 'slug', 'date_available']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'article', 'dynamicqueryset')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


admin.site.register(QuerySet, QuerySetAdmin)
admin.site.register(DynamicBox, DynamicBoxAdmin)
