#!/usr/bin/env python
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
