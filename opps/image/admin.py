# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User

from opps.image.models import Image


class ImagesAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        try:
            if obj.user:
                pass
        except User.DoesNotExist:
            obj.user = request.user

        super(ImagesAdmin, self).save_model(request, obj, form, change)



admin.site.register(Image, ImagesAdmin)
