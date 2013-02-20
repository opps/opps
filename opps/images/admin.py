# -*- coding: utf-8 -*-
from django.contrib import admin

from opps.images.models import Image, ImageCrop


class ImageCropAdmin(admin.ModelAdmin):
    pass
class ImagesAdmin(admin.ModelAdmin):
    pass


admin.site.register(ImageCrop, ImageCropAdmin)
admin.site.register(Image, ImagesAdmin)
