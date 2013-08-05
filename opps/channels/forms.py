#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Channel


class ChannelAdminForm(forms.ModelForm):
    layout = forms.ChoiceField(choices=(('default', _('Default'))))

    class Meta:
        model = Channel
