# -*- coding: utf-8 -*-
from django.contrib import admin

from opps.core.models import Channel


class ChannelAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Channel, ChannelAdmin)
