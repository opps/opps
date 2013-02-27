# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _



class Profile(models.Model):

    user = models.ForeignKey(User, related_name='user')
    twitter = models.CharField(_(u"Twitter"), max_length=75, blank=True,
            null=True)

    class Meta:
        app_label = 'opps'

    def __unicode__(self):
        return self.user
