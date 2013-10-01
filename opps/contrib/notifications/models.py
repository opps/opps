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

    def add(self, container, message, action='message', _type='json',
            **attrs):
        notification = Notification.objects.create(
            container=container,
            action=action,
            type=_type,
            message=message,
            **attrs
        )

        _db = Db(notification.container.get_absolute_url(),
                 notification.container.id)
        _db.publish(json.dumps({
            "action": notification.action,
            "id": notification.id,
            "published": notification.published,
            "date": notification.date_available,
            "message": notification.message}))
