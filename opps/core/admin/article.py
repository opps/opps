# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from opps.core.models import Post

from redactor.widgets import RedactorEditor



class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'content': RedactorEditor(),}


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()
admin.site.register(Post, PostAdmin)
