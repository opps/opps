# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User

from opps.core.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    pass


def user_unicode(self):
    return  u'{0}, {1}'.format(self.last_name, self.first_name)
User.__unicode__ = user_unicode

admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
