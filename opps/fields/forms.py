#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.functional import lazy

from .models import Field
from opps.core.forms import model_choices


class FieldAdminForm(forms.ModelForm):
    application = forms.ChoiceField(choices=lazy(model_choices, tuple)())

    class Meta:
        model = Field
