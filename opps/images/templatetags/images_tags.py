#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from ..generate import image_url as url


register = template.Library()


@register.simple_tag
def image_url(image_url, **kwargs):
    return url(image_url=image_url, **kwargs)


@register.simple_tag
def image_obj(image, **kwargs):
    if image == "":
        return ""
    if settings.THUMBOR_ENABLED:
        new = {}
        new['flip'] = image.flip
        new['flop'] = image.flop

        if image.halign != "":
            new['halign'] = image.halign
        if image.valign != "":
            new['valign'] = image.valign

        new['fit_in'] = image.fit_in
        new['smart'] = image.smart

        if image.crop_x1 > 0 or image.crop_x2 > 0 or image.crop_y1 > 0 or \
           image.crop_y2 > 0:
            new['crop'] = ((image.crop_x1, image.crop_y1),
                           (image.crop_x2, image.crop_y2))

        kwargs = dict(new, **kwargs)

    return url(image_url=image.archive.url, **kwargs)
