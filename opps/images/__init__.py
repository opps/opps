# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings



trans_app_label = _('Image')
settings.INSTALLED_APPS += ('sorl.thumbnail',)
