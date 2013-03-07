# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from opps.article.models import Post, PostImage, PostSource

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


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'content': RedactorEditor()}


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {"slug": ["title"]}
    list_display = ['title', 'channel', 'date_available', 'published']
    list_filter = ['date_available', 'published', 'channel']
    search_fields = ['title', 'headline']
    inlines = [PostImageInline, PostSourceInline]
    exclude = ('user',)
    raw_id_fields = ['main_image', 'channel']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('title', 'slug',)}),
        (_(u'Content'), {
            'fields': ('short_title', 'headline', 'content',
                'main_image')}),
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

        super(PostAdmin, self).save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
