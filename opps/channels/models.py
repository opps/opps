# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from mptt.models import MPTTModel, TreeForeignKey

from opps.core.models import Publishable, BaseConfig
from .utils import generate_long_slug


class ChannelManager(models.Manager):

    def get_homepage(self, site):
        try:
            return super(ChannelManager, self).get_query_set().filter(
                site=site, homepage=True, published=True).get()
        except Channel.DoesNotExist:
            return None


class Channel(MPTTModel, Publishable):

    name = models.CharField(_(u"Name"), max_length=60)
    slug = models.SlugField(u"URL", max_length=150, db_index=True)
    long_slug = models.SlugField(_(u"Path name"), max_length=250,
                                 db_index=True)
    description = models.CharField(_(u"Description"),
                                   max_length=255, null=True, blank=True)
    show_in_menu = models.BooleanField(_(u"Show in menu?"), default=False)
    homepage = models.BooleanField(_(u"Is home page?"), default=False)
    position = models.IntegerField(_(u"Position"), default=0)
    parent = TreeForeignKey('self', related_name='subchannel',
                                null=True, blank=True)

    objects = ChannelManager()

    class MPTTMeta:
        order_insertion_by = ['position', 'name']

    def __unicode__(self):
        if self.parent:
            return "%s/%s" % (self.parent, self.slug)
        return "%s/%s" % (self.site.domain, self.slug)

    def get_absolute_url(self):
        return "http://{0}/".format(self.__unicode__())

    def clean(self):

        try:
            channel_exist_domain = Channel.objects.filter(
                slug=self.slug,
                site__domain=self.site.domain)
            channel_is_home = Channel.objects.filter(site=self.site.id,
                                                     homepage=True,
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
            self.long_slug = generate_long_slug(self.parent, self.slug,
                                                self.site.domain)

        super(Channel, self).save(*args, **kwargs)


class ChannelConfig(BaseConfig):
    """
    Default implementation
    """
    pass
