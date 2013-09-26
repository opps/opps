#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin

from .forms import FieldAdminForm
from .models import Field, Option, FieldOption


class FieldOptionRelatedInline(admin.TabularInline):
    model = FieldOption
    fk_name = 'field'
    raw_id_fields = ['option']
    actions = None
    ordering = ('order',)
    extra = 1
    classes = ('collapse',)


class FieldAdmin(admin.ModelAdmin):
    form = FieldAdminForm
    prepopulated_fields = {"slug":
                           ["application", "type", "name"]}
    inlines = [FieldOptionRelatedInline]


admin.site.register(Field, FieldAdmin)
admin.site.register(Option)
