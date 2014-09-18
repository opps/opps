# -*- coding: utf-8 -*-

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_rss_link(context):
    try:
        rss_template = settings.OPPS_RSS_LINK_TEMPLATE
        rss_path = '#'
        if 'channel' in context:
            channel = context['channel']
            # TODO: Now by design homepage will always be named home
            # in future use get_homepage to determine the home page.
            if channel['level'] == 0 and channel['slug'] == 'home':
                rss_path = 'http://{0}/rss'.format(
                    context['site'].domain)
            else:
                rss_path = 'http://{0}/{1}/rss'.format(
                    context['site'].domain,
                    channel['long_slug']
                )
        else:
            raise Exception()
        return rss_template.format(rss_path)
    except:
        return ''
