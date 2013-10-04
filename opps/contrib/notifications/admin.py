#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Notification


class AdminNotification(admin.ModelAdmin):
    raw_id_fields = ('container',)


admin.site.register(Notification, AdminNotification)
