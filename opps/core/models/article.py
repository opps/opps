# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable
from opps.core.models import Channel
from opps.core.models.image import Image
from opps.core.models import Source

from tagging.fields import TagField



class Article(Publishable):

    title = models.CharField(_(u"Title"), max_length=140)
    slug = models.SlugField(_(u"URL"), max_length=150, unique=True,
            db_index=True)
    short_title = models.CharField(_(u"Short title"), max_length=140,
            blank=False, null=True)
    headline = models.TextField(_(u"Headline"), blank=True)
    channel = models.ForeignKey(Channel, verbose_name=_(u"Channel"))

    content = models.TextField(_(u"Content"))

    main_image = models.ForeignKey(Image, verbose_name=_(u'Main Image'),
            blank=False, null=True, on_delete=models.SET_NULL,
            related_name='article_main_image')

    sources = models.ManyToManyField(Source, null=True, blank=True,
            related_name='post_sources', through='PostSource')

    tags = TagField(null=True, verbose_name=_(u"Tags"))


    class Meta:
        abstract = True

    def __unicode__(self):
        return "{0}/{1}".format(self.channel, self.slug)


class Post(Article):

    images = models.ManyToManyField(Image, null=True, blank=True,
            related_name='post_images', through='PostImage')

    class Meta:
        app_label = 'core'


class PostImage(models.Model):
    post = models.ForeignKey(Post, verbose_name=_(u'Post'), null=True,
            blank=True, related_name='postimage_post',
            on_delete=models.SET_NULL)
    image = models.ForeignKey(Image, verbose_name=_(u'Image'), null=True,
            blank=True, related_name='postimage_image',
            on_delete=models.SET_NULL)
    order = models.PositiveIntegerField(_(u'Order'), default=1)

    def __unicode__(self):
        return self.image.title

    class Meta:
        app_label = 'core'


class PostSource(models.Model):
    post = models.ForeignKey(Post, verbose_name=_(u'Post'), null=True,
            blank=True, related_name='postsource_post',
            on_delete=models.SET_NULL)
    source = models.ForeignKey(Source, verbose_name=_(u'Source'), null=True,
            blank=True, related_name='postsource_source',
            on_delete=models.SET_NULL)
    order = models.PositiveIntegerField(_(u'Order'), default=1)

    def __unicode__(self):
        return self.source.slug

    class Meta:
        app_label = 'core'
