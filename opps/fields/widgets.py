#!/usr/bin/env python
# -*- coding: utf-8 -*
import json
from django import forms
from django.template.loader import render_to_string

from .models import Field, Option, FieldOption


class JSONField(forms.TextInput):
    model = Field
    def render(self, name, value, attrs=None):
        elements = []
        values = json.loads(value)
        objs = self.model.objects.all()
        for obj in objs:
            o = {}
            o['name'] = obj.name
            o['slug'] = obj.slug

            element_attr = {}
            element_attr['name'] = obj.name
            element_attr['slug'] = obj.slug
            """
            element_attr['value'] = '1'
            element_attr['obj_value'] = values.get(obj.slug, '')
            """

            if obj.type in ["checkbox", "radiobox"]:
                obj_value = []
                fo = FieldOption.objects.filter(field=obj)
                for i in fo:
                    key = "{}_{}".format(obj.slug, i.option.slug)
                    obj_value.append(values.get(key, ''))
                element_attr['list'] = zip(fo, obj_value)

            o['element'] = render_to_string(
                "admin/opps/fields/json_{}.html".format(obj.type),
                dictionary=element_attr
            )
            elements.append(o)

        return render_to_string(
            "admin/opps/fields/json.html",
            {"elements": elements,
             "name": name,
             "value": value})
