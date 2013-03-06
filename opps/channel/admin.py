# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User

from opps.channel.models import Channel
from opps.channel.utils import generate_long_slug


class ChannelAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name",)}
    exclude = ('user', 'long_slug')

    def save_model(self, request, obj, form, change):
        obj.long_slug = generate_long_slug(obj.channel, obj.slug,
                obj.site.domain)
        try:
            if obj.user:
                pass
        except User.DoesNotExist:
            obj.user = request.user

        super(ChannelAdmin, self).save_model(request, obj, form, change)


admin.site.register(Channel, ChannelAdmin)
