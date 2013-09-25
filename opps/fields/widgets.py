#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.template.loader import render_to_string

from .models import Field


class JSONField(forms.TextInput):
    model = Field
    def render(self, name, value, attrs=None):
        import pdb; pdb.set_trace()
        objs = self.model.objects.all()
        elements = []
        for obj in objs:
            o = {}
            o['name'] = obj.name
            o['slug'] = obj.slug
            o['element'] = render_to_string(
                "admin/opps/fields/json_{}.html".format(obj.type),
                {'slug': obj.slug, 'name': obj.name, 'value': 1}
            )
            elements.append(o)

        return render_to_string(
            "admin/opps/fields/json.html",
            {"elements": elements,
             "name": name,
             "value": value})
