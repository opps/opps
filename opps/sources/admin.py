# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Source
from opps.core.admin import PublishableAdmin


class SourceAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name']
    list_filter = ['date_available', 'published']
    exclude = ('user',)

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Content'), {
            'fields': ('url', 'feed')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


admin.site.register(Source, SourceAdmin)
