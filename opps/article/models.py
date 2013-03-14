# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Article
from opps.core.models import Publishable
from opps.image.models import Image
from opps.source.models import Source
from opps.channel.models import Channel


class Post(Article):

    images = models.ManyToManyField(Image, null=True, blank=True,
                                    related_name='post_images',
                                    through='PostImage')


class PostImage(models.Model):
    post = models.ForeignKey(Post, verbose_name=_(u'Post'), null=True,
                             blank=True, related_name='postimage_post',
                             on_delete=models.SET_NULL)
    image = models.ForeignKey(Image, verbose_name=_(u'Image'), null=True,
                              blank=True, related_name='postimage_image',
                              on_delete=models.SET_NULL)
    order = models.PositiveIntegerField(_(u'Order'), default=0)

    def __unicode__(self):
        return self.image.title


class PostSource(models.Model):
    post = models.ForeignKey(Post, verbose_name=_(u'Post'), null=True,
                             blank=True, related_name='postsource_post',
                             on_delete=models.SET_NULL)
    source = models.ForeignKey(Source, verbose_name=_(u'Source'), null=True,
                               blank=True, related_name='postsource_source',
                               on_delete=models.SET_NULL)
    order = models.PositiveIntegerField(_(u'Order'), default=0)

    def __unicode__(self):
        return self.source.slug


class ArticleBox(Publishable):
    name = models.CharField(_(u"Box name"), max_length=140)
    slug = models.SlugField(_(u"Slug"), max_length=150,
                            unique=True, db_index=True)
    posts = models.ManyToManyField(Post, null=True, blank=True,
                                   related_name='articlebox_post',
                                   through='ArticleBoxPost')

    def __unicode__(self):
        return self.slug


class ArticleBoxPost(models.Model):
    post = models.ForeignKey(Post, verbose_name=_(u'Article Box Post'), null=True,
                             blank=True, related_name='articleboxpost_post',
                             on_delete=models.SET_NULL)
    articlebox = models.ForeignKey(ArticleBox, verbose_name=_(u'Article Box'), null=True,
                                   blank=True, related_name='articlebox',
                                   on_delete=models.SET_NULL)


    def __unicode__(self):
        return "{0}-{1}".format(self.articlebox.slug, self.post.slug)
