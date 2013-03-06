# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from opps.core.models import Publishable
from opps.channel.utils import generate_long_slug



class Channel(Publishable):

    name = models.CharField(_(u"Name"), max_length=60, unique=True)
    slug = models.SlugField(u"URL", max_length=150, unique=True,
            db_index=True)
    long_slug = models.SlugField(_(u"Path name"), max_length=250, unique=True,
            db_index=True)
    description = models.CharField(_(u"Description"),
            max_length=255, null=True, blank=True)
    homepage = models.BooleanField(_(u"Is home page?"), default=False)
    position = models.IntegerField(_(u"Position"), default=1)
    channel = models.ForeignKey('self', related_name='subchannel',
            null=True, blank=True)

    def __unicode__(self):
        if self.channel:
            return "%s/%s" % (self.channel, self.slug)
        return "%s/%s" % (self.site.domain, self.slug)

    def clean(self):

        try:
            channel_exist_domain = Channel.objects.filter(slug=self.slug,
                    site__domain=self.site.domain)
            channel_is_home = Channel.objects.filter(homepage=True,
                    published=True).all()
            if self.pk:
                channel_is_home = channel_is_home.exclude(pk=self.pk)
        except ObjectDoesNotExist:
            return False

        if len(channel_exist_domain) >= 1 and not self.pk:
            raise ValidationError('Slug exist in domain!')

        if self.homepage and len(channel_is_home) >= 1:
            raise ValidationError('Exist home page!')

    def save(self, *args, **kwargs):

        if not self.long_slug:
            self.long_slug = generate_long_slug(self.channel, self.slug,
                    self.site.domain)

        super(Channel, self).save(*args, **kwargs)
