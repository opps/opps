#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.admin import SimpleListFilter
from django.core.files.images import get_image_dimensions

from .models import Image
from .forms import ImageModelForm
from .generate import image_url
from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules

User = get_user_model()


class UserListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _(u'User')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = u'user'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        # filter only users with images
        qs = User.objects.filter(image__isnull=False).distinct()
        if qs:
            return set([(item.username,
                         u"{0} ({1})".format(item.get_full_name(), item.email))
                       for item in qs])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == u"nouser":
            queryset = queryset.filter(user__isnull=True)
        elif self.value():
            queryset = queryset.filter(user__username=self.value())

        return queryset


@apply_opps_rules('images')
class ImagesAdmin(PublishableAdmin):
    form = ImageModelForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['image_thumb', 'image_dimension', 'title',
                    'date_available', 'published']
    list_filter = [UserListFilter, 'date_available', 'published']
    search_fields = ['title']
    raw_id_fields = ['source']
    readonly_fields = ['image_thumb']
    exclude = ('user',)

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'archive')}),
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
        '''.format(image_url(obj.archive.url),
                   'Select')
    opps_editor_select.short_description = _(u'Select')
    opps_editor_select.allow_tags = True

    def image_thumb(self, obj):
        if obj.archive:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.archive.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True

    def image_dimension(self, obj):
        try:
            width, height = get_image_dimensions(obj.archive)
            return u"{0}x{1}".format(width, height)
        except:
            return ''
    image_dimension.short_description = _(u'Dimension')

admin.site.register(Image, ImagesAdmin)
