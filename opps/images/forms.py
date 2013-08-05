#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from .models import Image
from .widgets import CropExample
# MultipleUpload,

from opps.core.widgets import OppsEditor


class ImageModelForm(forms.ModelForm):
    #archive = forms.FileField(required=True, widget=MultipleUpload())
    crop_example = forms.CharField(required=False, widget=CropExample())
    crop_x1 = forms.CharField(required=False, widget=forms.HiddenInput())
    crop_x2 = forms.CharField(required=False, widget=forms.HiddenInput())
    crop_y1 = forms.CharField(required=False, widget=forms.HiddenInput())
    crop_y2 = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Image
        widgets = {'description': OppsEditor()}

    # def more_image(self):
    #     more_image = self.files.getlist('image')[:]
    #     if len(more_image) >= 2:
    #         del more_image[-1]
    #         return more_image
    #     return []
