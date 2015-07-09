# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

from opps.core.models import Publishable
from opps.core.models import Slugged


CHANNEL_URL_NAME = \
    getattr(settings, 'OPPS_CHANNEL_URL_NAME', 'containers:channel')

URL_TARGET_CHOICES = (
    ('_blank', _(u'Load in a new window')),
    ('_self', _(u'Load in the same frame as it was clicked')),
    ('_parent', _(u'Load in the parent frameset')),
    ('_top', _(u'Load in the full body of the window'))
)


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

    main_image = models.ForeignKey(
        'images.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Main Image'),
    )

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

    menu_url_target = models.CharField(_(u"Menu URL Target"), max_length=255,
                                       choices=URL_TARGET_CHOICES,
                                       default="_self",
                                       null=True, blank=True)

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
        return u"/{0}/".format(self.long_slug)

    def get_absolute_url(self):
        url = reverse(CHANNEL_URL_NAME, args=(self.long_slug, ))
        return url

    def get_thumb(self):
        return None

    def get_http_absolute_url(self):
        return u"http://{0}{1}".format(self.site_domain,
                                       self.get_absolute_url())
    get_http_absolute_url.short_description = _(u'Get HTTP Absolute URL')

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains", "long_slug__icontains", )

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
            site__id=self.site.id,
            homepage=True, published=True)

        if self.pk:
            channel_is_home = channel_is_home.exclude(pk=self.pk)

        if self.homepage and channel_is_home.exists():
            raise ValidationError('Exist home page!')

        super(Channel, self).clean()

    def update_long_slug(self):
        if self.parent:
            self.long_slug = "{0}/{1}".format(
                self.parent.long_slug, self.slug)
        else:
            self.long_slug = self.slug

    def _set_long_slug(self):
        if self.parent:
            return u"{0}/{1}".format(self.parent.long_slug, self.slug)
        return self.slug

    def save(self, *args, **kwargs):
        self.long_slug = self._set_long_slug()
        super(Channel, self).save(*args, **kwargs)
