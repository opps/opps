#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _

from .models import QuerySet
from opps.core.forms import model_choices


class QuerySetAdminForm(forms.ModelForm):
    model = forms.ChoiceField(label=_(u'Model'),
                              choices=lazy(model_choices, tuple)())

    class Meta:
        model = QuerySet
