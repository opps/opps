#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import pkg_resources


pkg_resources.declare_namespace(__name__)
trans_app_label = _('Opps')

VERSION = (0, 1, 4)

__version__ = ".".join(map(str, VERSION))
__status__ = "Development"
__description__ = u"Opps CMS websites magazines and high-traffic"

__author__ = u"Thiago Avelino"
__credits__ = []
__email__ = u"opps-developers@googlegroups.com"
__license__ = u"MIT License"
__copyright__ = u"Copyright 2013, YACOWS"


settings.INSTALLED_APPS += (
    'opps.article',
    'opps.image',
    'opps.channel',
    'opps.source',
    'django.contrib.redirects',
    'django_thumbor',
    'googl',
    'redactor',
    'static_sitemaps',
    'tagging',)

settings.MIDDLEWARE_CLASSES += (
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',)

# Opps
getattr(settings, 'OPPS_SHORT', 'googl')
getattr(settings, 'OPPS_SHORT_URL', 'googl.short.GooglUrlShort')

# Sitemap
if not hasattr(settings, 'STATICSITEMAPS_ROOT_SITEMAP'):
    settings.STATICSITEMAPS_ROOT_SITEMAP = 'opps.sitemaps.feed.sitemaps'

# redactor
getattr(settings, 'REDACTOR_OPTIONS', {'lang': 'en'})
getattr(settings, 'REDACTOR_UPLOAD', 'uploads/')

# thumbor
getattr(settings, 'THUMBOR_SERVER', 'http://localhost:8888')
getattr(settings, 'THUMBOR_MEDIA_URL', 'http://localhost:8000/media')
getattr(settings, 'THUMBOR_SECURITY_KEY', '')
