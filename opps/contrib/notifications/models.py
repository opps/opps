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
    channel_long_slug = models.CharField(
        _(u"Channel long slug"),
        max_length=250,
        null=True, blank=True,
        db_index=True,
    )
    slug = models.SlugField(
        _(u"Slug"),
        max_length=150,
        null=True, blank=True,
        db_index=True,
    )

    action = models.CharField(_('Action'), max_length=75,
                              default="message")
    type = models.CharField(_('Type'), max_length=10,
                            choices=NOTIFICATION_TYPE,
                            default='json')
    message = models.TextField(_('Message'))

    def save(self, *args, **kwargs):
        self.channel_long_slug = self.container.channel_long_slug
        self.slug = self.container.slug
        super(Notification, self).save(*args, **kwargs)
        _db = Db(self.container.get_absolute_url(),
                 self.container.id)
        message = self.message
        if self.type == "json":
            message = json.dumps(self.message)
        _db.publish(json.dumps({
            "action": self.action,
            "id": self.id,
            "published": self.published,
            "date": self.date_available.strftime("%D %T"),
            "message": message}))
        _db.close()
