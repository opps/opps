# -*- coding: utf-8 -*-
from django.contrib import admin

from opps.core.models import Source

class SourceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Source, SourceAdmin)
