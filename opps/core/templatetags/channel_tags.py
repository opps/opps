# -*- coding: utf-8 -*-
from django import template
import logging

register = template.Library()
logger = logging.getLogger()


@register.simple_tag
def get_url(obj, http=False, target=None, url_only=False):

    if not hasattr(obj, 'child_class'):
        return obj.get_absolute_url()

    try:
        _url = obj.get_absolute_url()
        _target = target or '_self'
        _is_link = obj.child_class == 'Link'
        # Determine if it's a local or foreign link
        if _is_link and not obj.link.is_local() and not target:
            _target = '_blank'
        # Determine url type
        if http:
            _url = 'http://{}{}'.format(
                obj.site,
                obj.get_absolute_url())
        if url_only:
            return _url
        return 'href="{}" target="{}"'.format(_url, _target)
    except Exception as e:
        print str(e)
        logger.error("Exception at templatetag get_url: {}".format(e))
        return obj.get_absolute_url()
