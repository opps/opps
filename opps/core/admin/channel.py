# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User

from opps.core.models import Channel


class ChannelAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name",)}
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        try:
            if obj.user:
                pass
        except User.DoesNotExist:
            obj.user = request.user

        super(ChannelAdmin, self).save_model(request, obj, form, change)


admin.site.register(Channel, ChannelAdmin)
