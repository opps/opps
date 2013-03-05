#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings

VERSION = (0, 1, 2)

__version__ = ".".join(map(str, VERSION))
__status__ = "Development"
__description__ = u"Opps CMS websites magazines and high-traffic"

__author__ = u"Thiago Avelino"
__credits__ = []
__email__ = u"opps-developers@googlegroups.com"
__license__ = u"BSD"
__copyright__ = u"Copyright 2013, YACOWS"

settings.INSTALLED_APPS += ('opps.article',
        'opps.image',
        'opps.channel',
        'opps.source',
        'redactor',
        'tagging',)

settings.REDACTOR_OPTIONS = {'lang': 'en'}
settings.REDACTOR_UPLOAD = 'uploads/'
