# -*- coding: utf-8 -*-
#from django.contrib import admin
from .models import Post, Album, Link

from opps.contrib import admin

admin.site.register(Post)
admin.site.register(Album)
admin.site.register(Link)
