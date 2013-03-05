# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from opps.core.models import Publishable



class Channel(Publishable):

    name = models.CharField(_(u"Name"), max_length=60, unique=True)
    slug = models.SlugField(u"URL", max_length=150, unique=True,
            db_index=True)
    description = models.CharField(_(u"Description"),
            max_length=255, null=True, blank=True)
    position = models.IntegerField(_(u"Position"), default=1)
    channel = models.ForeignKey('self', related_name='subchannel',
            null=True, blank=True)

    def slug_name(self):
        return "{0}/{1}".format(self.channel, self.slug).replace(self.site.domain, '')

    def __unicode__(self):
        if self.channel:
            return "%s/%s" % (self.channel, self.slug)
        return "%s/%s" % (self.site.domain, self.slug)

    def clean(self):

        try:
            channel_exist_domain = Channel.objects.filter(slug=self.slug,
                    site__domain=self.site.domain)
            channel_home = Channel.objects.filter(site__domain=self.site.domain,
                    channel=None, published=True)
        except ObjectDoesNotExist:
            return False

        if len(channel_exist_domain) >= 1 and not self.pk:
            raise ValidationError('Slug exist in domain!')

        if not self.channel and len(channel_home) >= 1 and not self.pk:
            raise ValidationError('Exist home channel published!')
