# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from appconf import AppConf


trans_app_label = _('Core')


class OppsCoreConf(AppConf):
    DEFAULT_URLS = ('127.0.0.1', 'localhost',)
    SHORT = 'googl'
    SHORT_URL = 'googl.short.GooglUrlShort'
    CHANNEL_CONF = {}

    class Meta:
        prefix = 'opps'


class StaticSiteMapsConf(AppConf):
    ROOT_SITEMAP = 'opps.sitemaps.feed.sitemaps'

    class Meta:
        prefix = 'staticsitemaps'


class HaystackConf(AppConf):
    SITECONF = 'opps.search'
    SEARCH_ENGINE = 'dummy'

    class Meta:
        prefix = 'haystack'


class RedactorConf(AppConf):
    OPTIONS = {'lang': 'en'}
    UPLOAD = 'uploads/'

    class Meta:
        prefix = 'redactor'


class ThumborConf(AppConf):
    SERVER = 'http://localhost:8888'
    MEDIA_URL = 'http://localhost:8000/media'
    SECURITY_KEY = ''

    class Meta:
        prefix = 'thumbor'


class DjangoConf(AppConf):
    CACHES = {'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}


settings.INSTALLED_APPS += (
    'opps.channels',
    'opps.sources',
    'opps.articles',
    'opps.images',
    'opps.sitemaps',
    'appconf',
    'django.contrib.redirects',
    'django.contrib.sitemaps',
    'django_thumbor',
    'haystack',
    'googl',
    'redactor',
    'taggit',
    'mptt',)

settings.MIDDLEWARE_CLASSES += (
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'opps.core.middleware.DynamicSiteMiddleware',)

settings.TEMPLATE_CONTEXT_PROCESSORS += (
    'opps.channels.context_processors.channel_context',)
