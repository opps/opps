# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from opps.core.models import Config

register = template.Library()

CONFIG_DICT = getattr(settings, 'OPPS_GET_CONFIG_DICT', None)


@register.assignment_tag
def get_config(key, app_label=None, **kwargs):
    """
    {% load config %}
    {% get_config 'key_slug' %}
    {% get_config 'key_slug' app_label='promos'  %}
    {% get_config 'color' app_label='channels' channel__long_slug='/home' %}

    Also works
    {% get_config app_label='opps.polls' key='key_slug' %}
    """
    if CONFIG_DICT:
        try:
            channel = kwargs['channel__long_slug']
            value = CONFIG_DICT.get(channel, {}).get(key, None)
            if value:
                return value
        except:
            pass

    if app_label in ['none', 'null', 'None']:
        try:
            del kwargs['app_label']
        except:
            pass

    return Config.get_value(key, **kwargs)


@register.simple_tag
def get_configs(app_label, key_group, **kwargs):
    """
    {% load config %}
    {% get_configs 'polls' 'key_group_slug' %}
    {% get_configs 'infographics' 'key_group_slug' %}
    {% get_configs 'promos' 'key_group_slug' %}
    """

    if app_label in ['none', 'null', 'None']:
        try:
            del kwargs['app_label']
        except:
            pass

    return Config.get_values(key_group, **kwargs)
