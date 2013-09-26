#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin

from .forms import FieldAdminForm
from .models import Field


class FieldAdmin(admin.ModelAdmin):
    form = FieldAdminForm


admin.site.register(Field, FieldAdmin)
