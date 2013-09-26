#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from .models import Post, Album, Link

from opps.core.widgets import OppsEditor

from opps.db.models.fields.jsonf import JSONFormField
from opps.fields.widgets import JSONField
from opps.fields.models import Field, FieldOption


class PostAdminForm(forms.ModelForm):
    json = JSONFormField(widget=JSONField(), required=False)

    multiupload_link = '/fileupload/image/'

    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)

        for field in Field.objects.all():
            for fo in FieldOption.objects.filter(field=field):
                self.fields[
                    'json_{}_{}'.format(
                        field.slug, fo.option.slug
                    )] = forms.CharField(required=False)

    class Meta:
        model = Post
        widgets = {'content': OppsEditor()}


class AlbumAdminForm(forms.ModelForm):

    multiupload_link = '/fileupload/image/'

    class Meta:
        model = Album
        widgets = {
            'headline': OppsEditor()
        }


class LinkAdminForm(forms.ModelForm):
    class Meta:
        model = Link
