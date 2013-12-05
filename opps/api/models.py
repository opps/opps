#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import hmac

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

try:
    from hashlib import sha1
except ImportError:
    import sha
    sha1 = sha.sha


User = get_user_model()


class ApiKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    key = models.CharField(u"Key", max_length=255)
    date_insert = models.DateTimeField(u"Date insert", auto_now_add=True)

    def __unicode__(self):
        return u"{} for {}".format(self.key, self.user)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ApiKey, self).save(*args, **kwargs)

    def generate_key(self):
        new_uuid = uuid.uuid4()
        return hmac.new(new_uuid.bytes, digestmod=sha1).hexdigest()


def create_api_key(sender, **kwargs):
    if kwargs.get('created') is True:
        ApiKey.objects.create(user=kwargs.get('instance'))


models.signals.post_save.connect(create_api_key, settings.AUTH_USER_MODEL)
