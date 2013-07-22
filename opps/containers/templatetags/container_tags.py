# -*- coding: utf-8 -*-
from django import template


register = template.Library()


@register.assignment_tag
def get_recommendations(query_slice, child_class, container):
    """
    Takes the container object and get recommendations and filters by given
    child_class and limit the result by given slice.

    Sample usage::

        {% get_recommendations ":3" "post" container as context_var %}

    query_slice:
        A string with slice notation to limit the queryset result
    child_class:
        Name of child class
    container:
        A Container object
    """

    if not query_slice:
        query_slice = ":"

    bits = []
    for x in query_slice.split(':'):
        if len(x) == 0:
            bits.append(None)
        else:
            bits.append(int(x))

    return container.recommendation(child_class, bits)
