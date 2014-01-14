#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
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
    layout = models.CharField(_(u'Layout'), max_length=250, db_index=True,
                              default="default")
    description = models.CharField(_(u"Description"),
                                   max_length=255, null=True, blank=True)
    hat = models.CharField(_(u"Hat"),
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
                            null=True, blank=True,
                            verbose_name=_(u'Parent'))
    paginate_by = models.IntegerField(_("Paginate by"), null=True, blank=True)
    objects = ChannelManager()

    class Meta:
        unique_together = ("site", "long_slug", "slug", "parent")
        verbose_name = _(u'Channel')
        verbose_name_plural = _(u'Channels')
        ordering = ['name', 'parent__id', 'published']

    class MPTTMeta:
        unique_together = ("site", "long_slug", "slug", "parent")
        order_insertion_by = ['order']

    def __unicode__(self):
        """ Uniform resource identifier
        http://en.wikipedia.org/wiki/Uniform_resource_identifier
        """
        return u"/{}/".format(self._set_long_slug())

    def get_absolute_url(self):
        return u"{}".format(self.__unicode__())

    def get_thumb(self):
        return None

    def get_http_absolute_url(self):
        return u"http://{}{}".format(self.site_domain, self.get_absolute_url())
    get_http_absolute_url.short_description = _(u'Get HTTP Absolute URL')

    @property
    def search_category(self):
        """for use in search result"""
        return _(u'Channel')

    @property
    def title(self):
        return self.name

    @property
    def root(self):
        return self.get_root()

    def clean(self):
        channel_is_home = Channel.objects.filter(
            site__id=settings.SITE_ID,
            homepage=True, published=True)
        if self.pk:
            channel_is_home = channel_is_home.exclude(pk=self.pk)

        if self.homepage and channel_is_home.exists():
            raise ValidationError('Exist home page!')

        super(Channel, self).clean()

    def _set_long_slug(self):
        if self.parent:
            return u"{}/{}".format(self.parent.long_slug, self.slug)
        return u"{}".format(self.slug)

    def save(self, *args, **kwargs):
        self.long_slug = self._set_long_slug()
        super(Channel, self).save(*args, **kwargs)
