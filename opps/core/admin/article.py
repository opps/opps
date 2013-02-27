# -*- coding: utf-8 -*-
from django.contrib import admin

from opps.core.models import Post



class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
admin.site.register(Post, PostAdmin)
