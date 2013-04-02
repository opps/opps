# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .models import Post, Album, Article, ArticleSource, ArticleImage
from .models import ArticleBox, ArticleBoxArticles

from redactor.widgets import RedactorEditor


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


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_display = ['title', 'channel', 'date_available', 'published']
    list_filter = ['date_available', 'published', 'channel']
    search_fields = ['title', 'headline']
    readonly_fields = ['get_http_absolute_url', 'short_url']
    exclude = ('user',)
    raw_id_fields = ['main_image', 'channel']

    def save_model(self, request, obj, form, change):
        User = get_user_model()
        try:
            obj.site = obj.channel.site
            if obj.user:
                pass
        except User.DoesNotExist:
            obj.user = request.user

        super(ArticleAdmin, self).save_model(request, obj, form, change)


class PostAdmin(ArticleAdmin):
    form = PostAdminForm
    inlines = [ArticleImageInline, ArticleSourceInline]
    raw_id_fields = ['main_image', 'channel', 'album']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url')}),
        (_(u'Content'), {
            'fields': ('short_title', 'headline', 'content', 'main_image')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'album',)}),
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
            'fields': ('title', 'slug', 'get_http_absolute_url', 'short_url',)}),
        (_(u'Content'), {
            'fields': ('short_title', 'headline', 'main_image')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class ArticleBoxAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    inlines = [ArticleBoxArticlesInline]
    exclude = ('user',)
    raw_id_fields = ['channel', 'article']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'article')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def save_model(self, request, obj, form, change):
        User = get_user_model()
        try:
            if obj.user:
                pass
        except User.DoesNotExist:
            obj.user = request.user

        super(ArticleBoxAdmin, self).save_model(request, obj, form, change)


class HideArticleAdmin(admin.ModelAdmin):
    def get_model_perms(self, *args, **kwargs):
        return {}


admin.site.register(Article, HideArticleAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(ArticleBox, ArticleBoxAdmin)
