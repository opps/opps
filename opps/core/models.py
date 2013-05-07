#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.redirects.models import Redirect
from django.utils import timezone


class Date(models.Model):

    date_insert = models.DateTimeField(_(u"Date insert"), auto_now_add=True)
    date_update = models.DateTimeField(_(u"Date update"), auto_now=True)

    class Meta:
        abstract = True


class PublishableManager(models.Manager):
    def all_published(self):
        return super(PublishableManager, self).get_query_set().filter(
            date_available__lte=timezone.now(), published=True)


class Publishable(Date):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    site = models.ForeignKey(Site, default=1)
    date_available = models.DateTimeField(_(u"Date available"),
                                          default=timezone.now, null=True)
    published = models.BooleanField(_(u"Published"), default=False)

    objects = PublishableManager()
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True

    def is_published(self):
        return self.published and self.date_available <= timezone.now()


class Slugged(models.Model):

    slug = models.SlugField(
        _(u"URL"),
        db_index=True,
        max_length=150,
    )

    def clean(self):
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


class BaseBox(Publishable):
    name = models.CharField(_(u"Box name"), max_length=140)
    slug = models.SlugField(
        _(u"Slug"),
        db_index=True,
        max_length=150,
        unique=True,
    )
    article = models.ForeignKey(
        'articles.Article',
        null=True, blank=True,
        help_text=_(u'Only published article'),
        on_delete=models.SET_NULL
    )
    channel = models.ForeignKey(
        'channels.Channel',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    channel_name = models.CharField(
        _(u"Channel name"),
        max_length=140,
        null=True, blank=False,
        db_index=True,
    )
    channel_long_slug = models.CharField(
        _(u"Channel long slug"),
        max_length=250,
        null=True, blank=False,
        db_index=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.channel:
            self.channel_name = self.channel.name
            self.channel_long_slug = self.channel.long_slug
        super(BaseBox, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{0}-{1}".format(self.slug, self.site.name)


class BaseConfig(Publishable):
    """
    Basic key:value configuration for apps
    In admin it should be accessible only for users in developers group

    TODO:
    - Create base template filters
       {{ get_value|'key' }}
    - format_value for Json and Yaml
    - BaseConfigAdmin to show only for developers

    """

    FORMATS = (
        ('text', 'text'),
        ('json', 'json'),
        ('int', 'int'),
        ('float', 'float'),
        ('long', 'long'),
        ('comma', 'comma list'),
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

    article = models.ForeignKey(
        'articles.Article',
        null=True, blank=True,
        help_text=_(u'Only published article'),
        on_delete=models.SET_NULL
    )
    channel = models.ForeignKey(
        'channels.Channel',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True
        permissions = (("developer", "Developer"),)
        unique_together = ("key_group", "key", "site", "channel", "article")

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
            BaseConfig.format_value(self.value, self.format)
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
        data = {
            item['key']: {
                'raw': item['value'],
                'format': item['format'],
                'value': cls.format_value(item['value'], item['format'])
            } for item in itemsqs
        }
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
