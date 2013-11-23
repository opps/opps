#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pkg_resources

pkg_resources.declare_namespace(__name__)

VERSION = (0, 2, 3)

OPPS_CORE_APPS = (
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
    'opps.images',
    'opps.containers',
    'opps.boxes',
    'opps.channels',
    'opps.articles',
    'opps.sitemaps',
    'opps.flatpages',
    'opps.archives',
    'opps.views',
    'opps.fields',
    'opps.api',
    'opps.contrib.notifications',
)

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
