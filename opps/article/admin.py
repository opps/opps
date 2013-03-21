# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from opps.article.models import Post, PostImage, PostSource
from opps.article.models import ArticleBox, ArticleBoxPost

from redactor.widgets import RedactorEditor


class PostImageInline(admin.TabularInline):
    model = PostImage
    fk_name = 'post'
    raw_id_fields = ['image']
    actions = None
    extra = 1
    fieldsets = [(None, {'fields': ('image', 'order')})]


class PostSourceInline(admin.TabularInline):
    model = PostSource
    fk_name = 'post'
    raw_id_fields = ['source']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('source', 'order')})]


class ArticleBoxPostInline(admin.TabularInline):
    model = ArticleBoxPost
    fk_name = 'articlebox'
    raw_id_fields = ['post']
    actions = None
    extra = 1


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'content': RedactorEditor()}


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_display = ['title', 'channel', 'date_available', 'published']
    list_filter = ['date_available', 'published', 'channel']
    search_fields = ['title', 'headline']
    readonly_fields = ('get_absolute_url', 'short_url',)
    exclude = ('user',)
    raw_id_fields = ['main_image', 'channel']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('title', 'slug', 'get_absolute_url', 'short_url',)}),
        (_(u'Content'), {
            'fields': ('short_title', 'headline', 'content', 'main_image')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def save_model(self, request, obj, form, change):
        try:
            obj.site = obj.channel.site
            if obj.user:
                pass
        except User.DoesNotExist:
            obj.user = request.user

        super(ArticleAdmin, self).save_model(request, obj, form, change)


class PostAdmin(ArticleAdmin):
    form = PostAdminForm
    inlines = [PostImageInline, PostSourceInline]


class ArticleBoxAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    inlines = [ArticleBoxPostInline]
    exclude = ('user',)
    raw_id_fields = ['channel', 'post']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'post')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def save_model(self, request, obj, form, change):
        try:
            if obj.user:
                pass
        except User.DoesNotExist:
            obj.user = request.user

        super(ArticleBoxAdmin, self).save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)
admin.site.register(ArticleBox, ArticleBoxAdmin)
