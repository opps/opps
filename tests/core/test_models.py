#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Date, Publisher, Slugged, Channeling
from opps.core.models import Imaged, Config
from opps.channels.models import Channel
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model


class DateFields(TestCase):

    def test_date_insert(self):
        field = Date._meta.get_field_by_name('date_insert')[0]
        self.assertEqual(field.__class__, models.DateTimeField)
        self.assertTrue(field.auto_now_add)

    def test_date_update(self):
        field = Date._meta.get_field_by_name('date_update')[0]
        self.assertEqual(field.__class__, models.DateTimeField)
        self.assertTrue(field.auto_now)


class PublisherFields(TestCase):

    def test_site(self):
        field = Publisher._meta.get_field_by_name('site')[0]
        self.assertEqual(field.__class__, models.ForeignKey)

    def test_site_iid(self):
        field = Publisher._meta.get_field_by_name('site_iid')[0]
        self.assertEqual(field.__class__, models.PositiveIntegerField)
        self.assertEqual(field.max_length, 4)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertTrue(field.db_index)

    def test_site_domain(self):
        field = Publisher._meta.get_field_by_name('site_domain')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 100)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertTrue(field.db_index)

    def test_date_available(self):
        field = Publisher._meta.get_field_by_name('date_available')[0]
        self.assertEqual(field.__class__, models.DateTimeField)
        self.assertTrue(field.null)
        self.assertTrue(field.db_index)

    def test_published(self):
        field = Publisher._meta.get_field_by_name('published')[0]
        self.assertEqual(field.__class__, models.BooleanField)
        self.assertFalse(field.default)
        self.assertTrue(field.db_index)


class ChannelingFields(TestCase):

    def test_channel(self):
        field = Channeling._meta.get_field_by_name('channel')[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertEqual(field.verbose_name, _(u"Channel"))

    def test_channel_name(self):
        field = Channeling._meta.get_field_by_name('channel_name')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertTrue(field.db_index)

    def test_channel_long_slug(self):
        field = Channeling._meta.get_field_by_name('channel_long_slug')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 250)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertTrue(field.db_index)


class SluggedTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.slug = u'my-slug-9'
        self.channel = Channel.objects.create(
            name=u'Home', slug=self.slug, description=u'home page',
            site=self.site, user=self.user
        )

    def test_channel(self):
        field = Slugged._meta.get_field_by_name('slug')[0]
        self.assertEqual(field.__class__, models.SlugField)
        self.assertTrue(field.db_index)
        self.assertEqual(field.max_length, 150)

    def test_slug_validation(self):
        channel = Channel(
            name=u'Home', slug=self.slug, description=u'home page',
            site=self.site, user=self.user
        )
        channel.clean()
        self.assertEqual(channel.slug, 'my-slug-10')


class ImagedTest(TestCase):

    def test_main_image(self):
        field = Imaged._meta.get_field_by_name('main_image')[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertEqual(field.verbose_name, u'Main Image')
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_main_image_caption(self):
        field = Imaged._meta.get_field_by_name('main_image_caption')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_images(self):
        field = Imaged._meta.get_field_by_name('images')[0]
        self.assertEqual(field.__class__, models.ManyToManyField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)


class ConfigTest(TestCase):

    def test_app_label(self):
        field = Config._meta.get_field_by_name('app_label')[0]
        self.assertEqual(field.__class__, models.SlugField)
        self.assertEqual(field.max_length, 150)
        self.assertTrue(field.db_index)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_key_group(self):
        field = Config._meta.get_field_by_name('app_label')[0]
        self.assertEqual(field.__class__, models.SlugField)
        self.assertEqual(field.max_length, 150)
        self.assertTrue(field.db_index)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_app_key(self):
        field = Config._meta.get_field_by_name('key')[0]
        self.assertEqual(field.__class__, models.SlugField)
        self.assertEqual(field.max_length, 150)
        self.assertTrue(field.unique)

    def test_format(self):
        field = Config._meta.get_field_by_name('format')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 20)
        self.assertEqual(field.default, 'text')

    def test_value(self):
        field = Config._meta.get_field_by_name('value')[0]
        self.assertEqual(field.__class__, models.TextField)

    def test_description(self):
        field = Config._meta.get_field_by_name('description')[0]
        self.assertEqual(field.__class__, models.TextField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_container(self):
        field = Config._meta.get_field_by_name('container')[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertEqual(field.help_text, _(u'Only published container'))
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_channel(self):
        field = Config._meta.get_field_by_name('channel')[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
