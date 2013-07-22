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
    VIEWS_LIMIT = None
    PAGINATE_BY = 10
    PAGINATE_SUFFIX = u''
    PAGINATE_NOT_APP = []
    CHECK_MOBILE = False
    DOMAIN_MOBILE = u''
    PROTOCOL_MOBILE = u'http'
    ADMIN_RULES = {}
    RELATED_POSTS_PLACEHOLDER = "---related---"
    CACHE_PREFIX = 'opps'
    CACHE_EXPIRE = 300
    CACHE_EXPIRE_LIST = 300
    CACHE_EXPIRE_DETAIL = 300
    RSS_LINK_TEMPLATE = '<a href="{}" class="ir ico ico-rss">RSS</a>'
    LIST_MODELS = ('Post',)
    RECOMMENDATION_RANGE_DAYS = 180
    SMART_SLUG_ENABLED = True
    OPPS_EDITOR = {}

    class Meta:
        prefix = 'opps'


class StaticSiteMapsConf(AppConf):
    ROOT_SITEMAP = 'opps.sitemaps.feed.sitemaps'

    class Meta:
        prefix = 'staticsitemaps'


class HaystackConf(AppConf):
    CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        }
    }

    class Meta:
        prefix = 'haystack'


class ThumborConf(AppConf):
    SERVER = 'http://localhost:8888'
    MEDIA_URL = 'http://localhost:8000/media'
    SECURITY_KEY = ''
    ARGUMENTS = {}
    ENABLED = False

    class Meta:
        prefix = 'thumbor'


class DjangoConf(AppConf):
    CACHES = {'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}


settings.INSTALLED_APPS += (
    'appconf',
    'haystack',
    'googl',
    'mptt',)
