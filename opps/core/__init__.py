# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings



trans_app_label = _('Opps')

settings.INSTALLED_APPS += ('opps.article',
        'opps.image',
        'opps.channel',
        'opps.source',
        'redactor',
        'tagging',)

settings.REDACTOR_OPTIONS = {'lang': 'en'}
settings.REDACTOR_UPLOAD = 'uploads/'
