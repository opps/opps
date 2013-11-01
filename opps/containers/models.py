#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import celery
from hashlib import md5
from datetime import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
from django.template.defaultfilters import slugify

from polymorphic import PolymorphicModel
from polymorphic.showfields import ShowFieldContent

from opps.core.cache import _cache_key
from opps.core.models import Publishable, Slugged, Channeling, Imaged
from opps.core.tags.models import Tagged
from opps.db.models.fields import JSONField
from opps.boxes.models import BaseBox

from .signals import shorturl_generate, delete_container


@celery.task
def check_mirror_channel(container_id):
    instance = Container.objects.get(id=container_id)
    mirror_channel = instance.mirror_channel.all()
    old_mirror_channel = [
        c.id for c in Mirror.objects.filter(container=instance)]

    for _id in [i for i in old_mirror_channel if i not in mirror_channel]:
        m = Mirror.objects.get(id=_id)
        m.delete()

    for channel in mirror_channel:
        try:
            mirror = Mirror.objects.get(
                channel=channel,
                container=instance,
                slug=instance.slug,
                site=instance.site,
            )
            mirror.title = instance.title
            mirror.slug = instance.slug
            mirror.published = instance.published
            mirror.main_image = instance.main_image
            mirror.channel_long_slug = channel.long_slug
            mirror.channel_name = channel.name
            mirror.site = instance.site
            mirror.save()
        except Mirror.DoesNotExist:
            mirror = Mirror.objects.create(
                channel=channel,
                container=instance,
                user=instance.user,
                title=instance.title,
                slug=instance.slug,
                published=instance.published,
                channel_long_slug=channel.long_slug,
                channel_name=channel.name,
                site=instance.site,
                main_image=instance.main_image)


class Container(PolymorphicModel, ShowFieldContent, Publishable, Slugged,
                Channeling, Imaged, Tagged):
    title = models.CharField(_(u"Title"), max_length=140, db_index=True)
    hat = models.CharField(
        _(u"Hat"),
        max_length=140,
        null=True, blank=True,
    )
    short_url = models.URLField(
        _(u"Short URL"),
        null=True, blank=True,
    )
    child_class = models.CharField(
        _(u'Child class'),
        max_length=30,
        null=True, blank=True,
        db_index=True
    )
    child_module = models.CharField(
        _(u'Child module'),
        max_length=120,
        null=True, blank=True,
        db_index=True
    )
    child_app_label = models.CharField(
        _(u'Child app label'),
        max_length=30,
        null=True, blank=True,
        db_index=True
    )
    show_on_root_channel = models.BooleanField(
        _(u"Show on root channel?"),
        default=True
    )
    source = models.CharField(
        _('Source'),
        null=True, blank=True,
        max_length=255)
    json = JSONField(_(u"Customized"),
                     null=True, blank=True)

    def __unicode__(self):
        return u"{}".format(self.get_absolute_url())

    def __repr__(self):
        val = self.__unicode__()
        if isinstance(val, str):
            return val
        elif not isinstance(val, unicode):
            val = unicode(val)
        return val.encode('utf8')

    class Meta:
        ordering = ['-date_available']
        verbose_name = _(u'Container')
        verbose_name_plural = _(u'Containers')
        unique_together = ("site", "channel_long_slug", "slug")

    def save(self, *args, **kwargs):
        if not self.channel_name:
            self.channel_name = self.channel.name
        if not self.channel_long_slug:
            self.channel_long_slug = self.channel.long_slug
        self.child_class = self.__class__.__name__
        self.child_module = self.__class__.__module__
        self.child_app_label = self._meta.app_label
        if self.slug == u"":
            self.slug = slugify(self.title)

        models.signals.post_save.connect(shorturl_generate,
                                         sender=self.__class__)
        super(Container, self).save(*args, **kwargs)
        if settings.OPPS_MIRROR_CHANNEL and self.mirror_channel:
            check_mirror_channel.apply_async(
                kwargs=dict(container_id=self.id), countdown=15)

    def get_absolute_url(self):
        return u"/{}/{}.html".format(self.channel_long_slug, self.slug)

    def get_thumb(self):
        return self.main_image

    @property
    def search_category(self):
        """for use in search result"""
        return _(self.child_class)

    def get_http_absolute_url(self):
        return u"http://{}{}".format(self.site_domain, self.get_absolute_url())
    get_http_absolute_url.short_description = _(u'Get HTTP Absolute URL')

    def recommendation(self, child_class=False, query_slice=[None, 10]):

        if not child_class:
            child_class = self.child_class

        now = timezone.now()
        start = now - timezone.timedelta(
            days=settings.OPPS_RECOMMENDATION_RANGE_DAYS
        )

        cachekey = _cache_key(
            u'{}-recommendation'.format(self.__class__.__name__),
            self.__class__, self.site_domain,
            u"{}-{}-{}".format(child_class, self.channel_long_slug, self.slug))
        getcache = cache.get(cachekey)
        if getcache:
            return getcache

        containers = Container.objects.filter(
            site_domain=self.site_domain,
            child_class=child_class,
            channel_long_slug=self.channel_long_slug,
            date_available__range=(start, now),
            published=True
        ).exclude(pk=self.pk)

        tag_list = []
        if self.tags:
            tag_list = [t for t in self.tags.split(',')[:3]]
            containers = containers.filter(
                reduce(operator.or_, (Q(tags__contains=tag) for tag in
                                      tag_list)),
            )
        containers = containers.distinct().order_by(
            '-date_available')[slice(*query_slice)]

        _list = [a for a in containers]

        cache.set(cachekey, _list, 3600)
        return _list

    def inbox(self, containerbox=None):
        obj = ContainerBoxContainers.objects
        if containerbox:
            return obj.get(container=self.id,
                           containerbox__slug=containerbox)
        return obj.filter(container=self.id)

    def custom_fields(self):
        import json
        if not self.json:
            return
        return json.loads(self.json)


class ContainerImage(models.Model):
    container = models.ForeignKey(
        'containers.Container',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Container'),
    )
    order = models.PositiveIntegerField(_(u'Order'), default=0)
    image = models.ForeignKey(
        'images.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Image'),
    )

    caption = models.CharField(
        _(u"Caption"),
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _(u'Container image')
        verbose_name_plural = _(u'Container images')
        ordering = ('order',)

    def __unicode__(self):
        if self.image:
            return u"{}".format(self.image.title)
        return u'Id:{} - Order:{}'.format(self.id, self.order)


class ContainerBox(BaseBox):

    title = models.CharField(
        _(u"Title"),
        null=True,
        blank=True,
        max_length=140,
    )
    title_url = models.CharField(
        _(u"Title Link"),
        null=True,
        blank=True,
        max_length=250,
    )
    containers = models.ManyToManyField(
        'containers.Container',
        null=True, blank=True,
        verbose_name=_(u'Container'),
        related_name='containerbox_containers',
        through='containers.ContainerBoxContainers'
    )
    queryset = models.ForeignKey(
        'boxes.QuerySet',
        null=True, blank=True,
        related_name='containerbox_querysets',
        verbose_name=_(u'Query Set')
    )

    class Meta:
        verbose_name = _(u'Container box')
        verbose_name_plural = _(u'Containers boxes')

    def ordered_containers(self, field='order'):
        now = timezone.now()
        return self.containers.filter(
            models.Q(containerboxcontainers__date_end__gte=now) |
            models.Q(containerboxcontainers__date_end__isnull=True),
            published=True,
            date_available__lte=now,
            containerboxcontainers__date_available__lte=now
        ).order_by('containerboxcontainers__order').distinct()

    def ordered_box_containers(self):
        now = timezone.now()
        return self.containerboxcontainers_set.filter(
            models.Q(date_end__gte=now) |
            models.Q(date_end__isnull=True),
            date_available__lte=now
        ).order_by('order').distinct()

    def get_queryset(self):
        """
        for backwards compatibility
        """
        return self.queryset and self.queryset.get_queryset()


class ContainerBoxContainers(models.Model):
    containerbox = models.ForeignKey(
        'containers.ContainerBox',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Container Box'),
    )
    container = models.ForeignKey(
        'containers.Container',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Container'),
    )

    order = models.PositiveIntegerField(_(u'Order'), default=0)
    aggregate = models.BooleanField(_(u'Aggregate container'), default=False)
    highlight = models.BooleanField(_(u'Highlight container'), default=False)
    date_available = models.DateTimeField(_(u"Date available"),
                                          default=timezone.now, null=True)
    date_end = models.DateTimeField(_(u"End date"), null=True, blank=True)

    title = models.CharField(_(u"Title"), max_length=140,
                             null=True, blank=True)

    hat = models.CharField(
        _(u"Hat"),
        max_length=140,
        null=True, blank=True,
    )

    main_image = models.ForeignKey(
        'images.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Main Image'),
    )
    main_image_caption = models.CharField(
        _(u"Main Image Caption"),
        max_length=4000,
        blank=True,
        null=True,
        help_text=_(u'Maximum characters 4000'),
    )

    url = models.URLField(_(u"URL"), null=True, blank=True)

    class Meta:
        ordering = ('order',)
        verbose_name = _(u'Article box articles')
        verbose_name_plural = _(u'Article boxes articles')
        ordering = ('order', 'aggregate',)

    def __unicode__(self):
        if self.container:
            return u"{0}-{1}".format(self.containerbox.slug,
                                     self.container.slug)
        else:
            return u"{0}".format(self.containerbox.slug)

    def clean(self):
        if not self.container and not self.url:
            raise ValidationError(_(u'Please select a Container or insert a '
                                    u'URL!'))

        if self.container and not self.container.published:
            raise ValidationError(_(u'Article not published!'))


class Mirror(Container):
    container = models.ForeignKey('containers.Container',
                                  related_name='containers_mirror',
                                  verbose_name=_(u'Container'))


models.signals.post_delete.connect(delete_container, sender=Container)
