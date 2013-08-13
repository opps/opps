# -*- coding: utf-8 -*-
from urlparse import urlparse

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.cache import cache

from .signals import redirect_generate
from opps.containers.models import Container, ContainerImage
from opps.core.cache import _cache_key


class Article(Container):
    headline = models.TextField(
        _(u"Headline"),
        blank=True, null=True)
    short_title = models.CharField(
        _(u"Short title"),
        max_length=140,
        null=True, blank=True)

    class Meta:
        abstract = True


class Post(Article):
    content = models.TextField(_(u"Content"))
    albums = models.ManyToManyField(
        'articles.Album',
        null=True, blank=True,
        related_name='post_albums',
        verbose_name=_(u"Albums")
    )
    related_posts = models.ManyToManyField(
        'containers.Container',
        null=True, blank=True,
        related_name='post_relatedposts',
        through='articles.PostRelated',
    )

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def all_images(self):
        cachekey = _cache_key(
            '{}main-all_images'.format(self.__class__.__name__),
            self.__class__, self.site_domain,
            u"{}-{}".format(self.channel_long_slug, self.slug))
        getcache = cache.get(cachekey)
        if getcache:
            return getcache

        imgs = super(Post, self).all_images()

        albums = self.albums.filter(
            published=True,
            date_available__lte=timezone.now(),
        )

        for album in albums:
            images = album.images.select_related('source').filter(
                published=True,
                date_available__lte=timezone.now(),
            ).exclude(
                pk__in=[i.pk for i in imgs]
            )

            captions = {
                ci.image_id: ci.caption for ci in
                ContainerImage.objects.filter(
                    container_id=album.pk
                )
            }
            print captions

            for image in images:
                caption = captions.get(image.pk)
                if caption:
                    image.description = caption
                imgs.append(image)

        cache.set(cachekey, imgs)
        return imgs

    def ordered_related(self, field='order'):
        """
        used in template
        """
        return self.related_posts.filter(
            published=True,
            date_available__lte=timezone.now()
        ).order_by(
            'postrelated_related__order'
        ).distinct()


class PostRelated(models.Model):
    post = models.ForeignKey(
        'articles.Post',
        verbose_name=_(u'Post'),
        null=True,
        blank=True,
        related_name='postrelated_post',
        on_delete=models.SET_NULL
    )
    related = models.ForeignKey(
        'containers.Container',
        verbose_name=_(u'Related Post'),
        null=True,
        blank=True,
        related_name='postrelated_related',
        on_delete=models.SET_NULL
    )
    order = models.PositiveIntegerField(_(u'Order'), default=0)

    class Meta:
        verbose_name = _('Related content')
        verbose_name_plural = _('Related contents')
        ordering = ('order',)

    def __unicode__(self):
        return u"{0}->{1}".format(self.related.slug, self.post.slug)


class Album(Article):
    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')

    def get_absolute_url(self):
        return "/album/{}/{}".format(self.channel_long_slug, self.slug)


class Link(Article):
    url = models.URLField(_(u"URL"), null=True, blank=True)
    container = models.ForeignKey(
        'containers.Container',
        null=True, blank=True,
        related_name='link_containers'
    )

    class Meta:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def get_absolute_url(self):
        return "/link/{}/{}".format(
            self.channel_long_slug,
            self.slug
        )

    def is_local(self):
        try:
            url = urlparse(self.url)
            return url.netloc.replace('www', '') == self.site_domain
        except:
            return False

    def is_subdomain(self):
        return self.site_domain in self.url

    def clean(self):
        if not self.url and not self.container:
            raise ValidationError(_('URL field is required.'))

        self.url = self.url
        if self.container:
            self.url = self.container.get_absolute_url()


models.signals.post_save.connect(redirect_generate, sender=Link)
