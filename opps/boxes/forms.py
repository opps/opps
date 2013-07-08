#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.db import models

from django.utils.functional import lazy
from .models import QuerySet


def model_choices():
    try:
        return tuple([
            (u"{0}.{1}".format(app._meta.app_label, app._meta.object_name),
             u"{0} - {1}".format(app._meta.app_label, app._meta.object_name))
            for app in models.get_models() if 'opps.' in app.__module__])
    except ImportError:
        return tuple([])


class QuerySetAdminForm(forms.ModelForm):
    model = forms.ChoiceField(choices=lazy(model_choices, tuple)())

    class Meta:
        model = QuerySet
