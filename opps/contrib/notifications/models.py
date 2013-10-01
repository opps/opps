#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable
from opps.db import Db


NOTIFICATION_TYPE = (
    (u'json', _(u'JSON')),
    (u'text', _(u'Text')),
    (u'html', _(u'HTML')),
)


class Notification(Publishable):
    container = models.ForeignKey('containers.Container')
    action = models.CharField(_('Action'), max_length=75,
                              default="message")
    type = models.CharField(_('Type'), max_length=10,
                            choices=NOTIFICATION_TYPE,
                            type='json')
    message = models.TextField(_('Message'))

