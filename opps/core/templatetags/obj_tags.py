# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter
def ofKey(value, arg):
    if value:
        return value.get(arg)
    return ""


@register.filter
def callMethod(obj, args):
    arg = args.split(',')
    methodName = arg[0]
    method = getattr(obj, methodName)
    return method(arg[1])


@register.assignment_tag
def try_values(*args):
    """Return the first valid value"""

    for arg in args:
        if arg:
            return arg

    return ""


@register.assignment_tag
def cache_obj(obj):
    """Cache given obj"""

    if not obj:
        return ""

    return obj
