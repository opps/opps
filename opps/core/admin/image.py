# -*- coding: utf-8 -*-
from django.contrib import admin

from opps.core.models.image import Image


class ImagesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImagesAdmin)
