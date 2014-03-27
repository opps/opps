# coding: utf-8
from django import template

register = template.Library()


@register.simple_tag
def action_button_url(obj, url=None):
    url = url or ""
    return url.format(obj=obj)
