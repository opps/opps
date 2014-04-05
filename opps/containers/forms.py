#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from opps.db.models.fields.jsonf import JSONFormField
from opps.fields.widgets import JSONField
from opps.fields.models import Field, FieldOption

from .models import Container, ContainerBoxContainers


class ContainerBoxContainersInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContainerBoxContainersInlineForm,
              self).__init__(*args, **kwargs)
        self.fields['order'].widget.attrs['readonly'] = True

    class Meta:
        model = ContainerBoxContainers


class ContainerAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContainerAdminForm, self).__init__(*args, **kwargs)

        if not settings.OPPS_MIRROR_CHANNEL:
            self.fields['mirror_channel'].widget.attrs['disabled'] = True

        self.fields['json'] = JSONFormField(
            widget=JSONField(
                attrs={'_model': self._meta.model.__name__}),
            required=False)
        for field in Field.objects.filter(
                application__contains=self._meta.model.__name__):
            if field.type == 'checkbox':
                for fo in FieldOption.objects.filter(field=field):
                    self.fields[
                        'json_{}_{}'.format(
                            field.slug, fo.option.slug
                        )] = forms.CharField(required=False)
            else:
                self.fields[
                    'json_{}'.format(field.slug)
                ] = forms.CharField(required=False)

    class Meta:
        model = Container
