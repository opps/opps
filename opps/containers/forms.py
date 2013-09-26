#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from opps.db.models.fields.jsonf import JSONFormField
from opps.fields.widgets import JSONField
from opps.fields.models import Field, FieldOption


class ContainerAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContainerAdminForm, self).__init__(*args, **kwargs)

        self.fields['json'] = JSONFormField(
            widget=JSONField(
                attrs={'_model': self._meta.model.__name__}),
            required=False)
        for field in Field.objects.filter(
            application__contains=self._meta.model.__name__):
            for fo in FieldOption.objects.filter(field=field):
                self.fields[
                    'json_{}_{}'.format(
                        field.slug, fo.option.slug
                    )] = forms.CharField(required=False)
