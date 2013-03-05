# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Article
from opps.core.models.image import Image
from opps.core.models import Source



class Post(Article):

    images = models.ManyToManyField(Image, null=True, blank=True,
            related_name='post_images', through='PostImage')


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
