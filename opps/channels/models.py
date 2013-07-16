# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from opps.core.models import Publishable
from opps.core.models import Slugged


class ChannelManager(TreeManager):

    def get_homepage(self, site):
        try:
            return super(ChannelManager, self).get_query_set().filter(
                site__domain=site, homepage=True, published=True).get()
        except Channel.DoesNotExist:
            return None


class Channel(MPTTModel, Publishable, Slugged):

    name = models.CharField(_(u"Name"), max_length=60)
    long_slug = models.SlugField(_(u"Path name"), max_length=250,
                                 db_index=True)
    description = models.CharField(_(u"Description"),
                                   max_length=255, null=True, blank=True)
    show_in_menu = models.BooleanField(_(u"Show in menu?"), default=False)
    include_in_main_rss = models.BooleanField(
        _(u"Show in main RSS?"),
        default=True
    )
    homepage = models.BooleanField(
        _(u"Is home page?"),
        default=False,
        help_text=_(u'Check only if this channel is the homepage.'
                    u' Should have only one homepage per site')
    )
    group = models.BooleanField(_(u"Group sub-channel?"), default=False)
    order = models.IntegerField(_(u"Order"), default=0)
    parent = TreeForeignKey('self', related_name='subchannel',
                            null=True, blank=True)

    objects = ChannelManager()

    class META:
        unique_together = ("site", "long_slug", "slug", "parent")
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')

    class MPTTMeta:
        unique_together = ("site", "long_slug", "slug", "parent")
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

    @property
    def root(self):
        return self.get_root()

    def clean(self):
        channel_exist_domain = Channel.objects.filter(
            slug=self.slug, site=self.site)
        channel_is_home = Channel.objects.filter(
            site__id=settings.SITE_ID,
            homepage=True, published=True)
        if self.pk:
            channel_is_home = channel_is_home.exclude(pk=self.pk)

        if channel_exist_domain.exists() and not self.pk:
            raise ValidationError('Slug exist in domain!')

        if self.homepage and channel_is_home.exists():
            raise ValidationError('Exist home page!')

        super(Channel, self).clean()

    def save(self, *args, **kwargs):
        self.long_slug = u"{}".format(self.slug)
        if self.parent:
            self.long_slug = u"{}/{}".format(self.parent.slug, self.slug)
        super(Channel, self).save(*args, **kwargs)
