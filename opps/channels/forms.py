# -*- coding: utf-8 -*-

from django.conf import settings
from django import forms

from .models import Channel


class ChannelAdminForm(forms.ModelForm):
    layout = forms.ChoiceField(choices=settings.OPPS_CHANNEL_LAYOUT)

    def __init__(self, *args, **kwargs):
        super(ChannelAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['slug'].widget.attrs['readonly'] = True

    class Meta:
        model = Channel
