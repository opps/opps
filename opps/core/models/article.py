# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from opps.core.models.published import Published
from opps.core.models.date import Date
from opps.core.models.channel import Channel
from opps.core.models.image import Image

from tagging.models import Tag
from tagging.fields import TagField



class Article(Published, Date):

    title = models.CharField(_(u"Title"), max_length=140)
    slug = models.SlugField(_(u"URL"), max_length=150, unique=True,
            db_index=True)
    short_title = models.CharField(_(u"Short title"), max_length=140,
            blank=False, null=True)
    headline = models.TextField(_(u"Headline"), blank=True)
    channel = models.ForeignKey(Channel, verbose_name=_(u"Channel"))

    content = models.TextField(_(u"Content"))

    images = models.ManyToManyField(Image, through='ArticleImage',
            related_name='article_images')


    tags = TagField(null=True, verbose_name=_(u"Tags"))


    class Meta:
        abstract = True

    def __unicode__(self):
        return "{0}/{1}".format(self.site.name, self.slug)


class Post(Article):

    credit = models.CharField(_("Credit"), blank=True, max_length=255)

    class Meta:
        app_label = 'core'
