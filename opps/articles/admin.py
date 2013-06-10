# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .models import Post, PostRelated, Album, Link
from opps.containers.admin import ContainerAdmin, ContainerImageInline
from opps.containers.admin import ContainerSourceInline
from opps.core.admin import apply_opps_rules
from opps.contrib.multisite.admin import AdminViewPermission

from redactor.widgets import RedactorEditor


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'content': RedactorEditor()}


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
    form = PostAdminForm
    inlines = [ContainerImageInline, ContainerSourceInline, PostRelatedInline]
    raw_id_fields = ['main_image', 'channel', 'albums']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url')}),
        (_(u'Content'), {
            'fields': ('hat', 'short_title', 'headline', 'content',
                       ('main_image', 'image_thumb'), 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'albums',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel', 'in_containerboxes')}),
    )


class AlbumAdminForm(forms.ModelForm):
    class Meta:
        model = Album
        widgets = {
            'headline': RedactorEditor(
                redactor_options=settings.REDACTOR_SIMPLE
            )
        }


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
                       ('main_image', 'image_thumb'), 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel')}),
    )


class LinkAdminForm(forms.ModelForm):
    class Meta:
        model = Link


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
                       ('main_image', 'image_thumb'), 'tags')}),
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
