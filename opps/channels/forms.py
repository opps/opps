#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Channel


class ChannelAdminForm(forms.ModelForm):
    layout = forms.ChoiceField(choices=(('default', _('Default')),))

    def __init__(self, *args, **kwargs):
        super(ChannelAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['slug'].widget.attrs['readonly'] = True

    class Meta:
        model = Channel
