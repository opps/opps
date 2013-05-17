# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.utils import timezone

register = template.Library()

@register.simple_tag(takes_context=True)
def get_rss_path(context):
    try:
        rss_template = '<a href="{}" class="ir ico ico-rss">RSS</a>'
        rss_path = ''
        if 'channel' in context:
            channel = context['channel']
            if channel['level'] == 0 and channel['slug'] == 'home':
                rss_path = 'http://{}/rss'.format(
                    context['site'].domain)
            else:
                rss_path = 'http://{}/{}/rss'.format(
                        context['site'].domain,
                        channel['long_slug'])
        else:
            raise Exception()
        return rss_template.format(rss_path)
    except Exception as e:
       return ''