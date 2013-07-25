# -*- encoding: utf-8 -*-
from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_insert')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ["name"]}

    fieldsets = [(None, {'fields': ('name', 'slug',)})]

    class Meta:
        model = Tag

admin.site.register(Tag, TagAdmin)
