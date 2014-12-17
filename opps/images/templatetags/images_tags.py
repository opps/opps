# -*- coding: utf-8 -*-
from django import template
from django.template import Node, TemplateSyntaxError, Variable
from django.conf import settings
from django.utils.translation import ugettext as _
from ..generate import image_url as url


register = template.Library()


class AllImagesCheckPermissionForObjectsNode(Node):
    def __init__(self, obj, name):
        self.obj = Variable(obj)
        self.name = name

    def render(self, context):
        check_published = True

        try:
            user = context['request'].user
            if user.is_staff or user.is_superuser:
                check_published = False
        except:
            pass

        obj = self.obj.resolve(context)
        context[self.name] = obj.all_images(check_published)
        return ''


@register.tag(name='all_images_check_permission')
def all_images_check_permission(parser, token):
    """
    {% all_images_check_permission object as images %}
    """
    try:
        parans = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            _('tag requires exactly two arguments'))
    if len(parans) != 4:
        raise TemplateSyntaxError(
            _('tag requires exactly three arguments'))
    if parans[2] != 'as':
        raise TemplateSyntaxError(
            _("second argument to tag must be 'as'"))
    return AllImagesCheckPermissionForObjectsNode(parans[1], parans[3])


@register.simple_tag
def image_url(image_url, **kwargs):
    return url(image_url=image_url, **kwargs)


@register.simple_tag
def image_obj(image, **kwargs):
    HALIGN_VALUES = ("left", "center", "right")
    VALIGN_VALUES = ("top", "middle", "bottom")

    if image == "" or not image:
        return ""

    if settings.THUMBOR_ENABLED:
        new = {}
        new['flip'] = image.flip
        new['flop'] = image.flop

        if image.halign and image.halign in HALIGN_VALUES:
            new['halign'] = image.halign
        if image.valign and image.valign in VALIGN_VALUES:
            new['valign'] = image.valign

        new['fit_in'] = image.fit_in
        new['smart'] = image.smart

        if 'filters' in kwargs:
            kw = [kwargs['filters']]
            new['filters'] = kw
            del kwargs['filters']

        if image.crop_x1 > 0 or image.crop_x2 > 0 or image.crop_y1 > 0 or \
           image.crop_y2 > 0:
            new['crop'] = ((image.crop_x1, image.crop_y1),
                           (image.crop_x2, image.crop_y2))

        kwargs = dict(new, **kwargs)

    if image.archive_link and image.archive_link != "":
        return url(image_url=image.archive_link, **kwargs)

    return image.image_url(**kwargs)
