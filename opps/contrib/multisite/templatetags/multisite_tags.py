# -*- coding: utf-8 -*-
import logging

from django import template
from django.core.cache import cache
from django.contrib.sites.models import Site

register = template.Library()


@register.assignment_tag
def get_all_sites():
    """
    Takes the container object and get recommendations and filters by given
    child_class and limit the result by given slice.

    Sample usage::

        {% get_all_sites as context_var %}
    """

    return Site.objects.all()
