#!/usr/bin/env python
import sys

from django import VERSION
from django.conf import settings
from django.core.management import execute_from_command_line


if not settings.configured:
    settings.configure(
        DEBUG = False,
        SITE_ID = 1,
        SECRET_KEY = 'o29a3w)gmsf1d^)yjizb4=f751i*-j92%i1)1sx^_0q%wwwnxs',
        LANGUAGE_CODE = 'en-us',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        OPPS_DB_HOST='127.0.0.1',
        OPPS_DB_PORT=6379,
        OPPS_DB_NAME='opps',
        OPPS_DB_ENGINE='opps.db._redis.Redis',
        TEMPLATE_CONTEXT_PROCESSORS = (
            "django.contrib.auth.context_processors.auth",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.core.context_processors.static",
            "django.core.context_processors.request",
            'django.contrib.messages.context_processors.messages',
            'opps.channels.context_processors.channel_context',
        ),
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.contrib.redirects.middleware.RedirectFallbackMiddleware'
        ),
        INSTALLED_APPS = (
            'opps.contrib.admin',
            'opps.contrib.fileupload',
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.sites',
            'django.contrib.redirects',

            'opps.core',
            'opps.core.tags',
            'opps.containers',
            'opps.boxes',
            'opps.channels',
            'opps.articles',
            'opps.images',
            'opps.sitemaps',
            'opps.flatpages',
            'opps.archives',
            'opps.views',
            'opps.fields',
            'opps.db',
            'opps.contrib.notifications',

            'djcelery',
        ),
        ROOT_URLCONF = "opps.urls",
        TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner',
        STATIC_URL = '/static/',
        BROKER_BACKEND = "redis",
        REDIS_PORT = 6379,
        REDIS_HOST = "localhost",
        BROKER_URL = "redis://localhost:6379/0",
        REDIS_DB = 0,
        REDIS_CONNECT_RETRY = True,
        CELERY_RESULT_BACKEND ='redis',
        OPPS_MIRROR_CHANNEL = True,
    )


def runtests():
    argv = sys.argv[:1] + ['test'] + sys.argv[1:]
    if VERSION[2] <= 5:
        argv = sys.argv[:1] + ['test'] + ['core', 'containers', 'articles',
                                          'boxes', 'channels', 'images',
                                          'sitemaps', 'flatpages', 'archives',
                                          'views', 'fields', 'db', 'notifications']
    import pdb; pdb.set_trace()
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()

