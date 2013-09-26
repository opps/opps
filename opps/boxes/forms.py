#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.functional import lazy

from .models import QuerySet
from opps.core.forms import model_choices


class QuerySetAdminForm(forms.ModelForm):
    model = forms.ChoiceField(choices=lazy(model_choices, tuple)())

    class Meta:
        model = QuerySet
