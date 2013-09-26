#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.functional import lazy

from .models import Field
from opps.core.forms import model_choices


class FieldAdminForm(forms.ModelForm):
    application = forms.ChoiceField(choices=lazy(model_choices, tuple)())

    def __init__(self, *args, **kwargs):
        super(FieldAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['slug'].widget.attrs['readonly'] = True

    class Meta:
        model = Field
