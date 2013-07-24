# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.simple_tag
def action_button_url(url, object_id):
    return url % object_id
