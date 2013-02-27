# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _



class Source(models.Model):

    name = models.CharField(_(u"Name"), max_length=75)
    slug = models.SlugField(_(u"Slug"), max_length=100, unique=True,
            db_index=True)
    url = models.URLField(_(u'URL'), max_length=200, blank=True, null=True)
    feed = models.URLField(_(u'URL'), max_length=200, blank=True, null=True)


    class Meta:
        app_label = 'opps'

    def __unicode__(self):
        return self.slug
