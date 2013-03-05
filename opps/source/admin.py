# -*- coding: utf-8 -*-
from django.contrib import admin

from opps.source.models import Source


class SourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Source, SourceAdmin)
