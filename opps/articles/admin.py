#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Post, PostRelated, Album, Link
from .forms import PostAdminForm, AlbumAdminForm, LinkAdminForm

from opps.containers.admin import ContainerAdmin, ContainerImageInline
from opps.core.admin import apply_opps_rules
from opps.contrib.multisite.admin import AdminViewPermission
from opps.fields.models import Field, FieldOption


@apply_opps_rules('articles')
class PostRelatedInline(admin.TabularInline):
    model = PostRelated
    fk_name = 'post'
    raw_id_fields = ['related']
    actions = None
    ordering = ('order',)
    extra = 1
    classes = ('collapse',)
    verbose_name = _(u'Related post')
    verbose_name_plural = _(u'Related posts')


@apply_opps_rules('articles')
class PostAdmin(ContainerAdmin, AdminViewPermission):

    form = PostAdminForm
    inlines = [ContainerImageInline, PostRelatedInline]
    search_fields = ['title', 'headline', 'slug', 'channel_name']
    raw_id_fields = ['main_image', 'channel', 'albums']
    ordering = ('-date_available',)

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url')}),
        (_(u'Content'), {
            'fields': ('hat', 'short_title', 'headline', 'content',
                       ('main_image', 'main_image_caption',
                        'image_thumb'), 'source', 'tags')}),
        (_(u'Custom'), {
            'fields': ('json',)}),
        (_(u'Relationships'), {
            'fields': ('channel', 'albums',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel', 'in_containerboxes')}),
    )

    def save_model(self, request, obj, form, change):
        _json = {}
        for field in Field.objects.all():
            for fo in FieldOption.objects.filter(field=field):
                key = "{}_{}".format(field.slug, fo.option.slug)
                _json[key] = request.POST.get('json_{}'.format(key), '')

        obj.json = json.dumps(_json)
        obj.save()


@apply_opps_rules('articles')
class AlbumAdmin(ContainerAdmin, AdminViewPermission):

    form = AlbumAdminForm
    inlines = [ContainerImageInline]
    list_display = ['title', 'channel', 'images_count',
                    'date_available', 'published', 'preview_url']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url',)}),
        (_(u'Content'), {
            'fields': ('hat', 'short_title', 'headline',
                       ('main_image', 'main_image_caption',
                        'image_thumb'), 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel')}),
    )


@apply_opps_rules('articles')
class LinkAdmin(ContainerAdmin, AdminViewPermission):
    form = LinkAdminForm
    raw_id_fields = ['container', 'channel', 'main_image']
    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url',)}),
        (_(u'Content'), {
            'fields': ('hat', 'short_title', 'headline', 'url', 'container',
                       ('main_image', 'main_image_caption',
                        'image_thumb'), 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel')}),
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Link, LinkAdmin)
