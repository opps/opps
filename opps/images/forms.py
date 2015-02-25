#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from opps.core.widgets import OppsEditor

from .models import Image
from .widgets import CropExample


class ImageModelForm(forms.ModelForm):
    crop_example = forms.CharField(label=_('Crop Example'), required=False,
                                   widget=CropExample())
    crop_x1 = forms.CharField(label=_(u'Crop X1'), required=False,
                              widget=forms.HiddenInput())
    crop_x2 = forms.CharField(label=_(u'Crop X2'), required=False,
                              widget=forms.HiddenInput())
    crop_y1 = forms.CharField(label=_(u'Crop Y1'), required=False,
                              widget=forms.HiddenInput())
    crop_y2 = forms.CharField(label=_(u'Crop Y2'), required=False,
                              widget=forms.HiddenInput())

    archive = forms.ImageField(label=_('Archive'), required=True)

    class Meta:
        model = Image
        widgets = {'description': OppsEditor()}


class PopUpImageForm(ImageModelForm):

    source = forms.CharField(
        required=True,
        label=_(u'Source'),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PopUpImageForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(PopUpImageForm, self).save(commit=False)
        if not instance.pk:
            instance.published = True
            instance.user = self.user
            instance.save()
        return instance

    class Meta:
        model = Image
        widgets = {'description': OppsEditor()}
        fields = ('site', 'title', 'archive', 'description', 'tags',
                  'source')
