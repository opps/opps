#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Logging


class LoggingAdmin(admin.ModelAdmin):
    model = Logging
    raw_id_fields = ('user',)
    exclude = ('site_iid', 'site_domain', 'mirror_site')


admin.site.register(Logging, LoggingAdmin)
