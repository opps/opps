#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from .models import Post, Album, Link

from opps.core.widgets import OppsEditor


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'content': OppsEditor()}


class AlbumAdminForm(forms.ModelForm):
    class Meta:
        model = Album
        widgets = {
            'headline': OppsEditor()
        }


class LinkAdminForm(forms.ModelForm):
    class Meta:
        model = Link
