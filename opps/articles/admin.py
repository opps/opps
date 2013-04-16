# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Post, Album, Article, Link, ArticleSource, ArticleImage
from .models import ArticleBox, ArticleBoxArticles, ArticleConfig
from opps.core.admin import PublishableAdmin

from redactor.widgets import RedactorEditor
from django_thumbor import generate_url


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    fk_name = 'article'
    raw_id_fields = ['image']
    actions = None
    extra = 1
    fieldsets = [(None, {'fields': ('image', 'order')})]


class ArticleSourceInline(admin.TabularInline):
    model = ArticleSource
    fk_name = 'article'
    raw_id_fields = ['source']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('source', 'order')})]


class ArticleBoxArticlesInline(admin.TabularInline):
    model = ArticleBoxArticles
    fk_name = 'articlebox'
    raw_id_fields = ['article']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('article', 'order')})]


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'content': RedactorEditor()}


class ArticleAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ['get_http_absolute_url', 'short_url']
    raw_id_fields = ['main_image', 'channel']


class PostAdmin(ArticleAdmin):
    form = PostAdminForm
    inlines = [ArticleImageInline, ArticleSourceInline]
    raw_id_fields = ['main_image', 'channel', 'albums']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url')}),
        (_(u'Content'), {
            'fields': ('short_title', 'headline', 'content', 'main_image',
                       'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'albums',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class AlbumAdminForm(forms.ModelForm):
    class Meta:
        model = Album


class AlbumAdmin(ArticleAdmin):
    form = AlbumAdminForm
    inlines = [ArticleImageInline]

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('title', 'slug', 'get_http_absolute_url',
                       'short_url',)}),
        (_(u'Content'), {
            'fields': ('short_title', 'headline', 'main_image', 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class LinkAdmin(ArticleAdmin):
    raw_id_fields = ['articles']
    fieldsets = (
        (_(u'Identification'), {
            'fields': ('title', 'slug', 'get_http_absolute_url',
                       'short_url',)}),
        (_(u'Content'), {
            'fields': ('short_title', 'headline', 'url', 'articles',
                       'main_image', 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class ArticleBoxAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    inlines = [ArticleBoxArticlesInline]
    raw_id_fields = ['channel', 'article', 'queryset']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'article', 'queryset')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class HideArticleAdmin(PublishableAdmin):

    list_display = ['image_thumb', 'title', 'channel_name', 'date_available',
                    'published']
    readonly_fields = ['image_thumb']

    def image_thumb(self, obj):
        if obj.main_image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                generate_url(obj.main_image.image.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True

    def get_model_perms(self, *args, **kwargs):
        return {}

    def has_add_permission(self, request):
        return False


class ArticleConfigAdmin(PublishableAdmin):
    list_display = ['key', 'key_group', 'channel', 'date_insert',
                    'date_available', 'published']
    list_filter = ["key", 'key_group', "channel", "published"]
    search_fields = ["key", "key_group", "value"]


admin.site.register(Article, HideArticleAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(ArticleBox, ArticleBoxAdmin)
admin.site.register(ArticleConfig, ArticleConfigAdmin)
