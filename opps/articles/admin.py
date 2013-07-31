# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Post, PostRelated, Album, Link
from .forms import PostAdminForm, AlbumAdminForm, LinkAdminForm

from opps.containers.admin import ContainerAdmin, ContainerImageInline
from opps.containers.admin import ContainerSourceInline
from opps.core.admin import apply_opps_rules
from opps.contrib.multisite.admin import AdminViewPermission


@apply_opps_rules('articles')
class PostRelatedInline(admin.TabularInline):
    model = PostRelated
    fk_name = 'post'
    raw_id_fields = ['related']
    actions = None
    ordering = ('order',)
    extra = 1
    classes = ('collapse',)
    verbose_name = (u'Related post')
    verbose_name_plural = (u'Related posts')


@apply_opps_rules('articles')
class PostAdmin(ContainerAdmin, AdminViewPermission):

    action_buttons = [
        {"text": "Upload multiple images",
         "icon": "icon-picture",
         "url": '/fileupload/image/%s/',
         "class": "btn btn-success",
         "style": "",
         "title": "Click to add multiple images"},
    ]

    form = PostAdminForm
    inlines = [ContainerImageInline, ContainerSourceInline, PostRelatedInline]
    raw_id_fields = ['main_image', 'channel', 'albums']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url')}),
        (_(u'Content'), {
            'fields': ('hat', 'short_title', 'headline', 'content',
                       ('main_image', 'main_image_caption',
                        'image_thumb'), 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'albums',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel', 'in_containerboxes')}),
    )


@apply_opps_rules('articles')
class AlbumAdmin(ContainerAdmin, AdminViewPermission):

    action_buttons = [
        {"text": "Upload multiple images",
         "icon": "icon-picture",
         "url": '/fileupload/image/%s',
         "class": "btn btn-success",
         "style": "",
         "title": "Click to add multiple images"},
    ]

    form = AlbumAdminForm
    inlines = [ContainerImageInline, ContainerSourceInline]
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
