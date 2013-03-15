# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from googl.short import GooglUrlShort

from opps.core.models import Publishable


class Article(Publishable):

    title = models.CharField(_(u"Title"), max_length=140)
    slug = models.SlugField(_(u"URL"), max_length=150, unique=True,
                            db_index=True)
    short_url = models.URLField(_("Short URL"), blank=False, null=True)
    short_title = models.CharField(_(u"Short title"), max_length=140,
                                   blank=False, null=True)
    headline = models.TextField(_(u"Headline"), blank=True)
    channel = models.ForeignKey('channel.Channel', verbose_name=_(u"Channel"))

    content = models.TextField(_(u"Content"))

    main_image = models.ForeignKey('image.Image',
                                   verbose_name=_(u'Main Image'), blank=False,
                                   null=True, on_delete=models.SET_NULL,
                                   related_name='article_main_image')

    sources = models.ManyToManyField('source.Source', null=True, blank=True,
                                     related_name='post_sources',
                                     through='PostSource')

    tags = TagField(null=True, verbose_name=_(u"Tags"))

    class Meta:
        abstract = True

    def __absolute_url(self):
        return "{0}/{1}".format(self.channel, self.slug)

    def get_absolute_url(self):
        return "http://{0}".format(self.__absolute_url())
    get_absolute_url.short_description = 'URL'

    def __unicode__(self):
        return self.__absolute_url()

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = GooglUrlShort(self.get_absolute_url()).short()
        super(Article, self).save(*args, **kwargs)
