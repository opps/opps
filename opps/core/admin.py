#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin


class PublishableAdmin(admin.ModelAdmin):
    """
    Overrides standard admin.ModelAdmin save_model method
    It sets user (author) based on data from requet.
    """
    list_display = ['title', 'channel', 'date_available', 'published']
    list_filter = ['date_available', 'published', 'channel']
    search_fields = ['title', 'slug', 'headline', 'channel']
    exclude = ('user',)
    date_hierarchy = ('date_available')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'pk', None) is None:
            obj.user = request.user
        obj.save()
