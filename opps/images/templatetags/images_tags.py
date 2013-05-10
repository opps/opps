#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from ..generate import image_url as url


register = template.Library()


@register.simple_tag
def image_url(image_url, **kwargs):
    return url(image_url=image_url, **kwargs)


@register.simple_tag
def image_obj(image, **kwargs):
    new = {}
    new['flip'] = image.flip
    new['flop'] = image.flop
    if image.halign:
        new['halign'] = image.halign
    if image.valign:
        new['valign'] = image.valign
    new['fit_in'] = image.fit_in
    new['smart'] = image.smart

    kwargs = dict(new, **kwargs)
    return url(image_url=image.image.url, **kwargs)
