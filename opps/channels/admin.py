# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mptt.admin import MPTTModelAdmin

from .models import Channel
from .forms import ChannelAdminForm
from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules
from opps.core.permissions.admin import AdminViewPermission
from opps.core.utils import get_template_path

import json


@apply_opps_rules('channels')
class ChannelAdmin(PublishableAdmin, MPTTModelAdmin, AdminViewPermission):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'show_channel_path', 'get_parent', 'site',
                    'date_available', 'homepage', 'order', 'show_in_menu',
                    'published']
    list_filter = ['date_available', 'published', 'site', 'homepage', 'parent',
                   'show_in_menu']
    search_fields = ['name', 'slug', 'long_slug', 'description']
    exclude = ('user', 'long_slug')
    raw_id_fields = ['parent', 'main_image']
    form = ChannelAdminForm

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'parent', 'name', 'slug', 'layout', 'hat',
                       'description', 'tags', 'main_image',
                       'order', ('show_in_menu', 'menu_url_target'),
                       'include_in_main_rss', 'homepage', 'group',
                       'paginate_by')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def get_parent(self, obj):
        if obj.parent_id:
            long_slug, slug = obj.long_slug.rsplit("/", 1)
            return long_slug

    get_parent.admin_order_field = "parent"
    get_parent.short_description = "Parent"

    def show_channel_path(self, obj):
        return unicode(obj)
    show_channel_path.short_description = _(u'Channel Path')

    def save_model(self, request, obj, form, change):
        long_slug = u"{0}".format(obj.slug)
        if obj.parent:
            long_slug = u"{0}/{1}".format(obj.parent.slug, obj.slug)
        obj.long_slug = long_slug

        super(ChannelAdmin, self).save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ChannelAdmin, self).get_form(request, obj, **kwargs)

        channel_json = []

        def _get_template_path(_path):
            template = get_template_path(_path)
            with open(template) as f:
                _jsonData = f.read().replace('\n', '')
                return json.loads(_jsonData)

        def _get_json_channel(_obj):
            return _get_template_path(
                u'containers/{0}/channel.json'.format(_obj.long_slug))

        def _get_json_channel_recursivelly(_obj):
            channel_json = []
            try:
                channel_json = _get_json_channel(_obj)
            except:
                _is_root = _obj.is_root_node()
                if not _is_root:
                    channel_json = _get_json_channel_recursivelly(_obj.parent)
                elif _is_root:
                    try:
                        channel_json = _get_template_path(
                            u'containers/channel.json')
                    except:
                        pass
            finally:
                return channel_json

        channel_json = _get_json_channel_recursivelly(obj)

        if u'layout' in channel_json:
            layout_list = ['default'] + [l for l in channel_json['layout']]
            layout_choices = (
                (n, n.title()) for n in layout_list)

            form.base_fields['layout'].choices = layout_choices
        return form


admin.site.register(Channel, ChannelAdmin)
