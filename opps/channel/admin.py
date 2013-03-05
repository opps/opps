# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User

from opps.channel.models import Channel


class ChannelAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name",)}
    exclude = ('user', 'long_slug')

    def save_model(self, request, obj, form, change):
        obj.long_slug = "{0}{1}".format(
                "{0}/".format(obj.channel) if obj.channel else "", obj.slug)\
                .replace("{0}/".format(obj.site.domain), '')
        try:
            if obj.user:
                pass
        except User.DoesNotExist:
            obj.user = request.user

        super(ChannelAdmin, self).save_model(request, obj, form, change)


admin.site.register(Channel, ChannelAdmin)
