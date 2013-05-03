# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from opps.core.models import Publishable, BaseConfig
from opps.core.models import Slugged


class ChannelManager(TreeManager):

    def get_homepage(self, site):
        try:
            return super(ChannelManager, self).get_query_set().filter(
                site=site, homepage=True, published=True).get()
        except Channel.DoesNotExist:
            return None


class Channel(MPTTModel, Publishable, Slugged):

    name = models.CharField(_(u"Name"), max_length=60)
    long_slug = models.SlugField(_(u"Path name"), max_length=250,
                                 db_index=True)
    description = models.CharField(_(u"Description"),
                                   max_length=255, null=True, blank=True)
    show_in_menu = models.BooleanField(_(u"Show in menu?"), default=False)
    homepage = models.BooleanField(_(u"Is home page?"), default=False)
    group = models.BooleanField(_(u"Group sub-channel?"), default=False)
    order = models.IntegerField(_(u"Order"), default=0)
    parent = TreeForeignKey('self', related_name='subchannel',
                            null=True, blank=True)

    objects = ChannelManager()

    class MPTTMeta:
        order_insertion_by = ['order', 'name']

    def __unicode__(self):
        """ Uniform resource identifier
        http://en.wikipedia.org/wiki/Uniform_resource_identifier
        """
        if self.parent:
            return u"/{}/{}/".format(self.parent.slug, self.slug)
        return u"/{}/".format(self.slug)

    def get_absolute_url(self):
        return u"{}".format(self.__unicode__())

    def get_thumb(self):
        return None

    @property
    def search_category(self):
        """for use in search result"""
        return _('Channel')

    @property
    def title(self):
        return self.name

    def clean(self):

        try:
            channel_exist_domain = Channel.objects.filter(
                slug=self.slug,
                site__domain=self.site.domain)
            channel_is_home = Channel.objects.filter(
                site=self.site.id,
                homepage=True,
                published=True).select_related('publisher')
            if self.pk:
                channel_is_home = channel_is_home.exclude(pk=self.pk)
        except ObjectDoesNotExist:
            return False

        if len(channel_exist_domain) >= 1 and not self.pk:
            raise ValidationError('Slug exist in domain!')

        if self.homepage and len(channel_is_home) >= 1:
            raise ValidationError('Exist home page!')

        # every class which implements Slugged needs this in clean
        try:
            super(Channel, self).clean()
        except AttributeError:
            pass  # does not implement the clean method

    def save(self, *args, **kwargs):
        self.long_slug = u"{}".format(self.slug)
        if self.parent:
            self.long_slug = u"{}/{}".format(self.parent.slug, self.slug)
        super(Channel, self).save(*args, **kwargs)


class ChannelConfig(BaseConfig):
    """
    Default implementation
    """
    pass
