#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.redirects.models import Redirect
from django.utils import timezone
from django.utils.text import slugify

from .managers import PublishableManager
from .cache import _cache_key


class Date(models.Model):

    date_insert = models.DateTimeField(_(u"Date insert"), auto_now_add=True)
    date_update = models.DateTimeField(_(u"Date update"), auto_now=True)

    class Meta:
        abstract = True


class Owned(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True


class OwnedNotRequired(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True, null=True)

    class Meta:
        abstract = True


class Publisher(Date):

    site = models.ForeignKey(Site, default=1)
    site_iid = models.PositiveIntegerField(
        _(u"Site id"),
        max_length=4,
        null=True, blank=True,
        db_index=True)
    site_domain = models.CharField(
        _(u"Site domain"),
        max_length=100,
        null=True, blank=True,
        db_index=True)
    mirror_site = models.ManyToManyField(
        'sites.Site',
        related_name="%(app_label)s_%(class)s_mirror_site",
        null=True, blank=True,
        verbose_name=_(u"Mirror site"),
    )
    date_available = models.DateTimeField(
        _(u"Date available"),
        default=timezone.now,
        null=True,
        db_index=True)
    published = models.BooleanField(
        _(u"Published"),
        default=False,
        db_index=True)

    objects = PublishableManager()
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.site_domain = self.site.domain
        self.site_iid = self.site.id
        super(Publisher, self).save(*args, **kwargs)

    def is_published(self):
        return self.published and self.date_available <= timezone.now()


class Publishable(Owned, Publisher):
    class Meta:
        abstract = True


class NotUserPublishable(Publisher):
    class Meta:
        abstract = True


class ManyChanneling(models.Model):
    channel = models.ManyToManyField(
        'channels.Channel',
        verbose_name=_(u"Channels"),
        null=True, blank=True,
    )

    class Meta:
        abstract = True


class ManySites(models.Model):
    site = models.ManyToManyField(
        Site,
        verbose_name=_(u"Sites"),
        null=True, blank=True,
    )

    class Meta:
        abstract = True


class Channeling(models.Model):

    channel = models.ForeignKey(
        'channels.Channel',
        verbose_name=_(u"Channel"),
    )
    mirror_channel = models.ManyToManyField(
        'channels.Channel',
        related_name="%(app_label)s_%(class)s_mirror_channel",
        null=True, blank=True,
        verbose_name=_(u"Mirror channel"),
    )
    channel_name = models.CharField(
        _(u"Channel name"),
        max_length=140,
        null=True, blank=True,
        db_index=True,
    )
    channel_long_slug = models.CharField(
        _(u"Channel long slug"),
        max_length=250,
        null=True, blank=True,
        db_index=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.channel:
            self.channel_name = self.channel.name
            self.channel_long_slug = self.channel.long_slug
        super(Channeling, self).save(*args, **kwargs)


class Slugged(models.Model):

    slug = models.SlugField(
        _(u"Slug"),
        db_index=True,
        max_length=150,
    )

    def clean(self):

        if self.slug in ("", None):
            try:
                self.slug = slugify(self.title)
            except:
                self.slug = slugify(self.name)
            else:
                pass

        self.validate_slug()

        if hasattr(self, 'get_absolute_url'):
            try:
                path = self.get_absolute_url()
            except:
                path = self.slug  # when get_absolute_url fails

            site = self.site or Site.objects.get(pk=1)
            redirect = Redirect.objects.filter(
                site=site,
                old_path=path
            )
            if redirect.exists():
                raise ValidationError(
                    _(u"The URL already exists as a redirect")
                )

        try:
            super(Slugged, self).clean()
        except AttributeError:
            pass  # does not implement the clean method

    def validate_slug(self):
        slug = getattr(self, 'slug', None)
        site = getattr(self, 'site', None)

        filters = {'slug': slug, 'site': site}

        if hasattr(self, 'channel'):
            filters['channel'] = self.channel

        if hasattr(self, 'parent'):
            filters['parent'] = self.parent

        # if model does not have site
        if not getattr(self, 'site', False):
            del filters['site']

        slug_exists = self.__class__.objects.filter(**filters)

        if getattr(self, 'pk', None):
            slug_exists = slug_exists.exclude(pk=self.pk)

        if settings.OPPS_SMART_SLUG_ENABLED:
            if slug_exists:
                last = slug_exists.latest('slug').slug
                suffix = last.split('-')[-1]
                if suffix.isdigit():
                    suffix = int(suffix) + 1
                    self.slug = "{0}-{1}".format(
                        '-'.join(last.split('-')[0:-1]),
                        suffix
                    )
                else:
                    self.slug = "{0}-1".format(self.slug)
                return self.validate_slug()
        else:
            if slug_exists.exists():
                raise ValidationError(_(u"Slug already exists."))

    def save(self, *args, **kwargs):
        if hasattr(self, 'get_absolute_url'):
            model = self.__class__
            if self.pk is not None:
                old_object = model.objects.get(pk=self.pk)
                if old_object.slug != self.slug:
                    redirect = Redirect(
                        site=self.site,
                        old_path=old_object.get_absolute_url(),
                        new_path=self.get_absolute_url()
                    )
                    redirect.save()

        super(Slugged, self).save(*args, **kwargs)

    class Meta:
        unique_together = ['site', 'slug']
        abstract = True


class Imaged(models.Model):
    main_image = models.ForeignKey(
        'images.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_mainimage",
        verbose_name=_(u'Main Image'))

    main_image_caption = models.CharField(
        _(u"Main image caption"),
        max_length=255,
        blank=True,
        null=True
    )

    images = models.ManyToManyField(
        'images.Image',
        null=True, blank=True,
        through='containers.ContainerImage')

    class Meta:
        abstract = True

    def all_images(self, check_published=True):
        cachekey = _cache_key(
            '{0}-all_images'.format(self.__class__.__name__),
            self.__class__, self.site_domain,
            u"{0}-{1}".format(self.channel_long_slug, self.slug))
        getcache = cache.get(cachekey)
        if getcache and check_published:
            return getcache

        imgs = []

        if self.main_image:
            self.main_image.caption = self.main_image_caption
            imgs.append(self.main_image)

        images = self.images.filter(
            date_available__lte=timezone.now()
        ).order_by('containerimage__order')
        if check_published:
            images = images.filter(published=True)

        if self.main_image:
            images = images.exclude(pk=self.main_image.pk)
        imgs += [i for i in images.distinct()]

        captions = dict(
            (ci.image_id, ci.caption) for ci in self.containerimage_set.all())

        if self.main_image:
            captions[self.main_image.id] = self.main_image.caption

        for im in imgs:
            caption = captions.get(im.pk)
            if caption:
                im.description = caption

        cache.set(cachekey, imgs)
        return imgs

    def get_thumb(self):
        return self.main_image


class Config(Publishable):
    """
    Basic key:value configuration for apps
    In admin it should be accessible only for users in developers group

    """

    FORMATS = (
        ('text', 'text'),
        ('json', 'json'),
        ('int', 'int'),
        ('float', 'float'),
        ('long', 'long'),
        ('comma', 'comma list'),
    )

    app_label = models.SlugField(
        _(u"App label"),
        db_index=True,
        max_length=150,
        null=True,
        blank=True
    )

    key_group = models.SlugField(
        _(u"Config Key Group"),
        db_index=True,
        max_length=150,
        null=True,
        blank=True
    )

    key = models.SlugField(
        _(u"Config Key"),
        db_index=True,
        max_length=150,
        unique=True,
    )

    format = models.CharField(_(u"Format"), max_length=20,
                              choices=FORMATS, default='text')
    value = models.TextField(_(u"Config Value"))
    description = models.TextField(_(u"Description"), blank=True, null=True)

    container = models.ForeignKey(
        'containers.Container',
        null=True, blank=True,
        help_text=_(u'Only published container'),
        on_delete=models.SET_NULL,
        verbose_name=_(u'Container')
    )
    channel = models.ForeignKey(
        'channels.Channel',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Channel')
    )

    class Meta:
        verbose_name = _(u'Config')
        verbose_name_plural = _(u'Configs')
        unique_together = ("app_label", "key_group", "key",
                           "site", "channel", "container")

    def __unicode__(self):
        return u"{0}-{1}".format(self.key, self.value)

    @classmethod
    def format_value(cls, value, format):
        casts = {
            'text': lambda value: value,
            'int': lambda value: int(value),
            'float': lambda value: float(value),
            'long': lambda value: long(value),
            'comma': lambda value: value.strip().split(','),
            'json': lambda value: json.loads(value),
        }
        return casts.get(format, lambda value: value)(value)

    def clean(self):
        try:
            Config.format_value(self.value, self.format)
        except:
            raise ValidationError(
                _(u"Can't format the value to %s") % self.format
            )

    @classmethod
    def get_keys(cls, **kwargs):
        keysqs = cls.objects.values('key')
        if kwargs:
            keysqs = keysqs.filter(**kwargs)
        return [item['key'] for item in keysqs]

    @classmethod
    def get_items(cls, **kwargs):
        itemsqs = cls.objects.values('key', 'value', 'format')
        if kwargs:
            itemsqs = itemsqs.filter(**kwargs)
        data = dict(
            [(item['key'], {
                'raw': item['value'],
                'format': item['format'],
                'value': cls.format_value(item['value'], item['format'])
            }) for item in itemsqs])
        return data

    @classmethod
    def get_value(cls, key, **kwargs):
        """
        kwargs must have filters to QuerySet
           site, channel, article, format, description
           return a single formated value
        """
        instance = cls.objects.filter(
            key=key,
            published=True,
            date_available__lte=timezone.now()
        )
        if kwargs:
            instance = instance.filter(**kwargs)

        if not instance:
            return False
        else:
            instance = instance.latest('date_insert')

        # format
        value = cls.format_value(instance.value, instance.format)

        return value

    @classmethod
    def get_values(cls, key_group, **kwargs):
        """
        kwargs must have filters to QuerySet
           site, channel, article, format, description
           return a dict of keys and formated values
        """
        instances = cls.objects.filter(
            key_group=key_group,
            published=True,
            date_available__lte=timezone.now()
        )
        if kwargs:
            instances = instances.filter(**kwargs)

        if not instances:
            return False

        value = {}
        for instance in instances:
            value[instance.key] = cls.format_value(instance.value,
                                                   instance.format)

        return value
