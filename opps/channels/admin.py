# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Channel
from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules


@apply_opps_rules('channels')
class ChannelAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'parent', 'site', 'date_available', 'homepage',
                    'order', 'published']
    list_filter = ['date_available', 'published', 'site', 'homepage', 'parent']
    search_fields = ['name']
    exclude = ('user', 'long_slug')
    raw_id_fields = ['parent']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'parent', 'name', 'slug', 'description',
                       'order', ('show_in_menu', 'include_in_main_rss'),
                       'homepage', 'group')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def save_model(self, request, obj, form, change):
        long_slug = u"{}".format(obj.slug)
        if obj.parent:
            long_slug = u"{}/{}".format(obj.parent.slug, obj.slug)
        obj.long_slug = long_slug

        super(ChannelAdmin, self).save_model(request, obj, form, change)


admin.site.register(Channel, ChannelAdmin)
