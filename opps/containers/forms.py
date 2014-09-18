# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

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
                        'json_{0}_{1}'.format(
                            field.slug, fo.option.slug
                        )] = forms.CharField(required=False)
            else:
                self.fields[
                    'json_{0}'.format(field.slug)
                ] = forms.CharField(required=False)

    def clean(self):
        msg = _('The slug "%s" already exists on channel "%s" at site "%s"')
        data = self.cleaned_data
        if data.get('site') and data.get('channel') and data.get('slug'):
            qs = Container.objects.filter(
                site=data['site'], channel=data['channel'], slug=data['slug'])
            if self.instance.pk is not None:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                args = (data['slug'], data['channel'], data['site'])
                msg = msg % args
                self._errors["slug"] = self.error_class([msg])
        return data

    class Meta:
        model = Container
