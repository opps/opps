# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .models import Channel, ChannelConfig
from .utils import generate_long_slug


class ChannelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'parent', 'site', 'date_available', 'homepage',
                    'position', 'published']
    list_filter = ['date_available', 'published', 'site', 'homepage', 'parent']
    search_fields = ['name']
    exclude = ('user', 'long_slug')
    raw_id_fields = ['parent']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'parent', 'name', 'slug', 'description',
                       'position', 'show_in_menu', 'homepage',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def save_model(self, request, obj, form, change):
        obj.long_slug = generate_long_slug(obj.parent, obj.slug,
                                           obj.site.domain)
        User = get_user_model()
        try:
            if obj.user:
                pass
        except User.DoesNotExist:
            obj.user = request.user

        super(ChannelAdmin, self).save_model(request, obj, form, change)


class ChannelConfigAdmin(admin.ModelAdmin):
    list_display = ['key', 'key_group', 'channel', 'date_insert',
                    'date_available', 'published']
    list_filter = ["key", 'key_group', "channel", "published"]
    search_fields = ["key", "key_group", "value"]
    raw_id_fields = ['channel']
    exclude = ('user', 'article')

    def save_model(self, request, obj, form, change):
        User = get_user_model()
        try:
            if obj.user:
                pass
        except User.DoesNotExist:
            obj.user = request.user

        super(ChannelConfigAdmin, self).save_model(request, obj, form, change)


admin.site.register(Channel, ChannelAdmin)
admin.site.register(ChannelConfig, ChannelConfigAdmin)
