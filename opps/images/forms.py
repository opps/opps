#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from .models import Image
from .widgets import MultipleUpload, CropExample
from opps.articles.utils import normalize_tags

from redactor.widgets import RedactorEditor


class ImageModelForm(forms.ModelForm):
    image = forms.FileField(required=True, widget=MultipleUpload())
    crop_example = forms.CharField(required=False, widget=CropExample())
    crop_x1 = forms.CharField(required=False, widget=forms.HiddenInput())
    crop_x2 = forms.CharField(required=False, widget=forms.HiddenInput())
    crop_y1 = forms.CharField(required=False, widget=forms.HiddenInput())
    crop_y2 = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Image
        widgets = {'description': RedactorEditor()}

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['tags'] = normalize_tags(u",".join(cleaned_data['tags']))
        return cleaned_data

    def more_image(self):
        more_image = self.files.getlist('image')[:]
        if len(more_image) >= 2:
            del more_image[-1]
            return more_image
        return []
