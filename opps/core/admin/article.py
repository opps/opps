# -*- coding: utf-8 -*-
from django.contrib import admin

from opps.core.models import Post



class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()
admin.site.register(Post, PostAdmin)
