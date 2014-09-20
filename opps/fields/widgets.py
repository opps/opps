#!/usr/bin/env python
# -*- coding: utf-8 -*
import json
from django import forms
from django.template.loader import render_to_string

from .models import Field, FieldOption
from opps.core.widgets import CONFIG


class JSONField(forms.TextInput):
    model = Field

    def render(self, name, value, attrs=None):
        elements = []
        try:
            values = json.loads(value)
        except TypeError:
            values = {}

        # value sometimes come as unicode and we need to treat it
        if type(values) == unicode:
            values = json.loads(values)

        objs = self.model.objects.filter(
            application__contains=self.attrs.get('_model', None))

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
            element_attr['obj_value'] = values.get(obj.slug, '')

            if obj.type in ["checkbox", "radio"]:
                fo = FieldOption.objects.filter(field=obj)
                if obj.type == "checkbox":
                    obj_value = []
                    for i in fo:
                        key = "{0}_{1}".format(obj.slug, i.option.slug)
                        obj_value.append(values.get(key, ''))
                    element_attr['list'] = zip(fo, obj_value)
                    del element_attr['obj_value']
                else:
                    element_attr['list'] = fo

            o['element'] = render_to_string(
                "admin/opps/fields/json_{0}.html".format(obj.type),
                dictionary=element_attr
            )
            elements.append(o)

        # OPPS Editor params
        # This is ugly as hell but for now it was the only way of getting this
        # working DRY
        js = CONFIG.get('js')[0]
        # must pass an string with commas on plugins
        plugins = ''
        for item in CONFIG.get('plugins'):
            line = ','.join(item.split())
            line += ','
            plugins += line
        language = CONFIG.get('language')
        theme = CONFIG.get('theme', 'modern')
        file_browser_callback = CONFIG.get('file_browser_callback')

        return render_to_string(
            "admin/opps/fields/json.html",
            {"elements": elements,
             "name": name,
             "value": value,
             "js": js,
             "theme": theme,
             "plugins": plugins,
             "language": language,
             "file_browser_callback": file_browser_callback,
             })
