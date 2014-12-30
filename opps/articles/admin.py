#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Post, PostRelated, Album, Link
from .forms import PostAdminForm, AlbumAdminForm, LinkAdminForm

from opps.containers.admin import (
    ContainerAdmin, ContainerImageInline, ContainerRelatedInline)
from opps.core.admin import apply_opps_rules, HaystackModelAdmin
from opps.core.permissions.admin import AdminViewPermission


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
class PostAdmin(HaystackModelAdmin, ContainerAdmin, AdminViewPermission):

    form = PostAdminForm
    inlines = [ContainerImageInline, ContainerRelatedInline]
    search_fields = ['title', 'headline', 'slug', 'channel_name']
    raw_id_fields = ['main_image', 'channel',
                     'mirror_channel', 'albums']
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
            'fields': ('channel', 'mirror_channel', 'albums',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel', 'in_containerboxes')}),
    )


@apply_opps_rules('articles')
class AlbumAdmin(HaystackModelAdmin, ContainerAdmin, AdminViewPermission):

    form = AlbumAdminForm
    inlines = [ContainerImageInline, ContainerRelatedInline]
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
        (_(u'Custom'), {
            'fields': ('json',)}),
        (_(u'Relationships'), {
            'fields': ('channel', 'mirror_channel')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel')}),
    )


@apply_opps_rules('articles')
class LinkAdmin(ContainerAdmin, AdminViewPermission):
    form = LinkAdminForm
    raw_id_fields = ['container', 'channel',
                     'mirror_channel', 'main_image']
    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url',)}),
        (_(u'Content'), {
            'fields': ('hat', 'short_title', 'headline', 'url', 'container',
                       ('main_image', 'main_image_caption',
                        'image_thumb'), 'tags')}),
        (_(u'Custom'), {
            'fields': ('json',)}),
        (_(u'Relationships'), {
            'fields': ('channel', 'mirror_channel')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel')}),
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Link, LinkAdmin)
