# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

from channels.models import Channel


register = template.Library()


@register.assignment_tag
def get_channel(slug):
    """
        Usage:

        {% get_channel "videos" %}
    """
    try:
        return Channel.objects.get(site=settings.SITE_ID, slug=slug,
                                   published=True)
    except:
        return Channel.objects.none()
