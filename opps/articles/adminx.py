# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from .models import Post, Album, Link

from opps.containers.models import ContainerSource, ContainerImage
from opps.contrib import admin
from opps.contrib.admin.layout import *
from xadmin.plugins.inline import Inline


class ImageInline(object):
    model = ContainerImage
    style = 'accordion'


class SourceInline(object):
    model = ContainerSource
    style = 'accordion'


class PostAdmin(object):
    raw_id_fields = ['main_image', 'channel', 'albums']
    inlines = [ImageInline, SourceInline]
    style_fields = {'system': "radio-inline"}

    form_layout = (
        Main(
            TabHolder(
                Tab(_(u'Identification'),
                    Fieldset('site', 'title', 'slug',
                    'get_http_absolute_url', 'short_url'),
                ),
                Tab(_(u'Content'),
                    Fieldset('hat', 'short_title', 'headline',
                    'content', 'main_image', 'main_image_caption',
                    'image_thumb' 'tags'),
                    Inline(ContainerImage),
                    Inline(ContainerSource),
                ),
                Tab(_(u'Relationships'),
                    Fieldset('channel', 'albums'),
                ),
        )),
        Side(
            Fieldset(_(u'Publication'), 'published', 'date_available',
                     'show_on_root_channel', 'in_containerboxes')

        )
    )

    reversion_enable = True


admin.site.register(Post, PostAdmin)
admin.site.register(Album)
admin.site.register(Link)
