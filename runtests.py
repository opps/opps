#!/usr/bin/env python
import sys

from django.conf import settings
from django.core.management import execute_from_command_line


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.contrib.redirects.middleware.RedirectFallbackMiddleware'
        ),
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'opps.contrib.admin',
            'opps.contrib.fileupload',
            'django.contrib.admin',
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
        ),
        SITE_ID = 1,
        ROOT_URLCONF = "opps.urls",
        TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner',
    )


def runtests():
    argv = sys.argv[:1] + ['test'] + ['core', 'containers', 'articles',
                                      'boxes', 'channels', 'images',
                                      'sitemaps', 'flatpages', 'archives']
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()

