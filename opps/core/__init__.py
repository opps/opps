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
    'tagging',)

settings.MIDDLEWARE_CLASSES += (
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',)

# Opps
getattr(settings, 'OPPS_SHORT', 'googl')
getattr(settings, 'OPPS_SHORT_URL', 'googl.short.GooglUrlShort')

# Sitemap
if not hasattr(settings, 'STATICSITEMAPS_ROOT_SITEMAP'):
    settings.STATICSITEMAPS_ROOT_SITEMAP = 'opps.sitemaps.feed.sitemaps'

# Haystack
getattr(settings, 'HAYSTACK_CONNECTIONS', {
    'default': {'ENGINE': 'haystack.backends.simple_backend.SimpleEngine'}})

# redactor
getattr(settings, 'REDACTOR_OPTIONS', {'lang': 'en'})
getattr(settings, 'REDACTOR_UPLOAD', 'uploads/')

# thumbor
getattr(settings, 'THUMBOR_SERVER', 'http://localhost:8888')
getattr(settings, 'THUMBOR_MEDIA_URL', 'http://localhost:8000/media')
getattr(settings, 'THUMBOR_SECURITY_KEY', '')
