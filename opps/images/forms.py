#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Image
from .widgets import CropExample

from opps.core.widgets import OppsEditor


class ImageModelForm(forms.ModelForm):
    crop_example = forms.CharField(
        required=False,
        widget=CropExample(),
        label=_(u'Exemplo de crop')
    )
    crop_x1 = forms.CharField(required=False, widget=forms.HiddenInput())
    crop_x2 = forms.CharField(required=False, widget=forms.HiddenInput())
    crop_y1 = forms.CharField(required=False, widget=forms.HiddenInput())
    crop_y2 = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Image
        widgets = {'description': OppsEditor()}

    def __init__(self, *args, **kwargs):
        super(ImageModelForm, self).__init__(*args, **kwargs)
        # if self.instance.pk:
        #     self.fields['generate_article'].widget = forms.HiddenInput()

    def more_image(self):
        more_image = self.files.getlist('image')[:]
        if len(more_image) >= 2:
            del more_image[-1]
            return more_image
        return []
