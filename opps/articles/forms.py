#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from .models import Post, Album, Link

from redactor.widgets import RedactorEditor


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'content': RedactorEditor()}


class AlbumAdminForm(forms.ModelForm):
    class Meta:
        model = Album
        widgets = {
            'headline': RedactorEditor(
                redactor_options=settings.REDACTOR_SIMPLE
            )
        }


class LinkAdminForm(forms.ModelForm):
    class Meta:
        model = Link
