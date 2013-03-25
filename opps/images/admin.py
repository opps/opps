# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import Image


class ImagesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'source', 'date_available', 'published']
    list_filter = ['date_available', 'published', 'source']
    search_fields = ['title']
    raw_id_fields = ['source']
    exclude = ('user',)

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'image')}),
        (_(u'Content'), {
            'fields': ('description', 'source')}),
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

        super(ImagesAdmin, self).save_model(request, obj, form, change)


admin.site.register(Image, ImagesAdmin)
