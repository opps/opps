# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from opps.source.models import Source


class SourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name',]
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


    def save_model(self, request, obj, form, change):
        try:
            if obj.user:
                pass
        except User.DoesNotExist:
            obj.user = request.user

        super(SourceAdmin, self).save_model(request, obj, form, change)

admin.site.register(Source, SourceAdmin)
