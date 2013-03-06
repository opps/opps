# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings



trans_app_label = _('Opps')

settings.INSTALLED_APPS += ('opps.article',
        'opps.image',
        'opps.channel',
        'opps.source',
        'django.contrib.redirects',
        'django_thumbor',
        'redactor',
        'tagging',)

settings.MIDDLEWARE_CLASSES += (
        'django.contrib.redirects.middleware.RedirectFallbackMiddleware',)

# redactor
settings.REDACTOR_OPTIONS = {'lang': 'en'}
settings.REDACTOR_UPLOAD = 'uploads/'

# thumbor
settings.THUMBOR_SERVER = 'http://localhost:8888'
settings.THUMBOR_MEDIA_URL = 'http://localhost:8000/media'
