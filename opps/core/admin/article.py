# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from opps.core.models import Post, PostImage, PostSource

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
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PostImageInline, PostSourceInline]

    fieldsets = (
            (None, {'fields': ('title', 'short_title', 'headline', 'channel',
                'content',)}),
            (None, {'fields': ('main_image', 'slug',)})
    )

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()
admin.site.register(Post, PostAdmin)
