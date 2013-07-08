# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils import timezone

from opps.core.utils import get_app_model


register = template.Library()


@register.simple_tag(takes_context=True)
def get_box(context, appname, slug, template_name=None):
    """
    {% load box_tags %}
    {% get_box 'polls' 'box_slug' %}
    """
    model = get_app_model(appname, "Box")
    try:
        box = model.objects.get(site=settings.SITE_ID, slug=slug,
                                date_available__lte=timezone.now(),
                                published=True)
    except model.DoesNotExist:
        box = None

    if template_name:
        t = template.loader.get_template(template_name)
    else:
        t = template.loader.get_template(
            '{0}/{1}_detail.html'.format(appname, model.__name__.lower())
        )
    return t.render(template.Context({'{0}'.format(
        model.__name__.lower()): box, 'slug': slug, 'context': context}))


@register.simple_tag(takes_context=True)
def get_all_box(context, appname, channel_long_slug, template_name=None):
    """
    {% load box_tags %}
    {% get_all_box 'polls' 'channel_slug' %}
    """
    model = get_app_model(appname, "Box")
    boxes = model.objects.filter(site=settings.SITE_ID,
                                 date_available__lte=timezone.now(),
                                 published=True,
                                 channel_long_slug=channel_long_slug)

    if template_name:
        t = template.loader.get_template(template_name)
    else:
        t = template.loader.get_template(
            '{0}/{1}_list.html'.format(appname, model.__name__.lower())
        )

    return t.render(template.Context({'{0}boxes'.format(
        model.__name__.lower()): boxes, 'context': context}))
