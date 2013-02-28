# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from opps.core.models import Post, PostImage
from opps.core.models import Image

from redactor.widgets import RedactorEditor



class PostImageInline(admin.TabularInline):
    model = PostImage
    fk_name = 'post'
    raw_id_fields = ['image']
    actions = None
    extra = 1
    fieldsets = [(None, {'fields': ('image', 'order')})]


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'content': RedactorEditor(),}


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PostImageInline]

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()
admin.site.register(Post, PostAdmin)
