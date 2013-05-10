#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from .models import Image
from .widgets import MultipleUpload, CropExample


class ImageModelForm(forms.ModelForm):
    image = forms.FileField(required=True, widget=MultipleUpload())
    crop_example = forms.CharField(required=False, widget=CropExample())

    class Meta:
        model = Image

    def more_image(self):
        more_image = self.files.getlist('image')[:]
        if len(more_image) >= 2:
            del more_image[-1]
            return more_image
        return []
