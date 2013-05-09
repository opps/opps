#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from ..generate import image_url as url


register = template.Library()

@register.simple_tag
def image_url(image_url, **kwargs):
    return url(image_url=image_url, **kwargs)
