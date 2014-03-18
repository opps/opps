#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pkg_resources

pkg_resources.declare_namespace(__name__)

VERSION = (0, 2, 4)

OPPS_CORE_APPS = [
    # Django core
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',

    # Admin
    'opps.contrib.admin',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',

    # Opps core
    'opps.core',
    'opps.core.tags',
    'opps.containers',
    'opps.boxes',
    'opps.channels',
    'opps.containers',
    'opps.articles',
    'opps.archives',
    'opps.images',
    'opps.sitemaps',
    'opps.flatpages',
    'opps.archives',
    'opps.fields',
    'opps.api',

    # Opps contrib
    'opps.contrib.fileupload',

    # Dependence
    'south',
    'appconf',
    'haystack',
    'mptt',
    'googl',
    'djcelery',
]

__version__ = ".".join(map(str, VERSION))
__status__ = "Development"
__description__ = u"Open Source Content Management Platform - CMS for the "
u"magazines, newspappers websites and portals with "
u"high-traffic, using the Django Framework."

__author__ = u"Thiago Avelino"
__credits__ = ['Bruno Rocha']
__email__ = u"opps-developers@googlegroups.com"
__license__ = u"MIT License"
__copyright__ = u"Copyright 2013, Opps Project"
