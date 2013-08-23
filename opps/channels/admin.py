# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Channel
from .forms import ChannelAdminForm
from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules
from opps.core.utils import get_template_path

import json


@apply_opps_rules('channels')
class ChannelAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'parent', 'site', 'date_available', 'homepage',
                    'order', 'show_in_menu', 'published']
    list_filter = ['date_available', 'published', 'site', 'homepage', 'parent']
    search_fields = ['name']
    exclude = ('user', 'long_slug')
    raw_id_fields = ['parent']
    form = ChannelAdminForm

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'parent', 'name', 'slug', 'layout',
                       'description', 'order', ('show_in_menu',
                                                'include_in_main_rss'),
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

    def get_form(self, request, obj=None, **kwargs):
        form = super(ChannelAdmin, self).get_form(request, obj, **kwargs)
        try:
            template = get_template_path(
                u'containers/{}/channel.json'.format(obj.slug))
            f = open(template)
            channel_json = json.loads(f.read().replace('\n', ''))
            f.close()
        except:
            channel_json = []

        if u'layout' in channel_json:
            layout_list = ['default'] + [l for l in channel_json['layout']]
            layout_choices = (
                (n, n.title()) for n in layout_list)

            form.base_fields['layout'].choices = layout_choices
        return form


admin.site.register(Channel, ChannelAdmin)
