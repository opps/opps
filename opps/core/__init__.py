# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


trans_app_label = _('Core')

settings.INSTALLED_APPS += (
    'opps.article',
    'opps.image',
    'opps.channel',
    'opps.source',
    'django.contrib.redirects',
    'django_thumbor',
    'haystack',
    'googl',
    'redactor',
    'static_sitemaps',
    'tagging',
    'mptt',)

settings.MIDDLEWARE_CLASSES += (
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'opps.core.middleware.DynamicSiteMiddleware',)

settings.TEMPLATE_CONTEXT_PROCESSORS += (
    'opps.channel.context_processors.channel_context',)

# Opps
settings.OPPS_DEFAULT_URLS = getattr(
    settings, 'OPPS_DEFAULT_URLS', ('127.0.0.1',))

settings.OPPS_SHORT = getattr(
    settings, 'OPPS_SHORT', 'googl')

settings.OOPS_SHORT_URL = getattr(
    settings, 'OPPS_SHORT_URL', 'googl.short.GooglUrlShort')

# Sitemap
settings.STATICSITEMAPS_ROOT_SITEMAP = getattr(
    settings, 'STATICSITEMAPS_ROOT_SITEMAP', 'opps.sitemaps.feed.sitemaps')

# Haystack
settings.HAYSTACK_SITECONF = getattr(
    settings, 'HAYSTACK_SITECONF', 'opps.search')

settings.HAYSTACK_SEARCH_ENGINE = getattr(
    settings, 'HAYSTACK_SEARCH_ENGINE', 'dummy')

# redactor
settings.REDACTOR_OPTIONS = getattr(
    settings, 'REDACTOR_OPTIONS', {'lang': 'en'})

settings.REDACTOR_UPLOAD = getattr(
    settings, 'REDACTOR_UPLOAD', 'uploads/')

# thumbor
settings.THUMBOR_SERVER = getattr(
    settings, 'THUMBOR_SERVER', 'http://localhost:8888')

settings.THUMBOR_MEDIA_URL = getattr(
    settings, 'THUMBOR_MEDIA_URL', 'http://localhost:8000/media')

settings.THUMBOR_SECURITY_KEY = getattr(
    settings, 'THUMBOR_SECURITY_KEY', '')
