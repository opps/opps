#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.files.images import get_image_dimensions

from .models import Image
from .forms import ImageModelForm
from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules
from opps.core.filters import UserListFilter


@apply_opps_rules('images')
class ImagesAdmin(PublishableAdmin):
    form = ImageModelForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['image_thumb', 'image_dimension', 'title',
                    'date_available', 'published']
    list_filter = [UserListFilter, 'date_available', 'published']
    search_fields = ['title', 'slug']
    readonly_fields = ['image_thumb']
    exclude = ('user',)

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'archive', 'archive_link')}),
        (_(u'Crop'), {
            'fields': ('flip', 'flop', 'halign', 'valign', 'fit_in',
                       'smart', 'crop_x1', 'crop_x2', 'crop_y1', 'crop_y2',
                       'crop_example')}),
        (_(u'Content'), {
            'fields': ('description', 'tags', 'source')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def get_list_display(self, request):
        list_display = self.list_display
        pop = request.GET.get('pop')
        if pop == u'oppseditor':
            list_display = ['opps_editor_select'] + list(list_display)
        return list_display

    def opps_editor_select(self, obj):
        return u'''
        <a href="#" onclick="top.opps_editor_popup_selector('{0}')">{1}</a>
        '''.format(obj.image_url(), 'Select')
    opps_editor_select.short_description = _(u'Select')
    opps_editor_select.allow_tags = True

    def image_thumb(self, obj):
        if obj.archive or obj.archive_link:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                obj.image_url(width=60, height=60)
            )
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True

    def image_dimension(self, obj):
        if obj.archive:
            try:
                width, height = get_image_dimensions(obj.archive)
                return u"{0}x{1}".format(width, height)
            except:
                return ''
        return ''

    image_dimension.short_description = _(u'Dimension')

admin.site.register(Image, ImagesAdmin)
