#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import hmac

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

try:
    from hashlib import sha1
except ImportError:
    import sha
    sha1 = sha.sha


User = get_user_model()


class ApiKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_(u"User"))
    key = models.CharField(_(u"Key"), max_length=255)
    date_insert = models.DateTimeField(_(u"Date insert"), auto_now_add=True)

    def __unicode__(self):
        return u"{0} for {1}".format(self.key, self.user)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ApiKey, self).save(*args, **kwargs)

    def generate_key(self):
        new_uuid = uuid.uuid4()
        return hmac.new(new_uuid.bytes, digestmod=sha1).hexdigest()

    class Meta:
        verbose_name = _(u"API Key")
        verbose_name_plural = _(u"API Keys")


def create_api_key(sender, **kwargs):
    if kwargs.get('created') is True:
        ApiKey.objects.create(user=kwargs.get('instance'))


if 'opps.api' in settings.INSTALLED_APPS:
    models.signals.post_save.connect(create_api_key, User)
