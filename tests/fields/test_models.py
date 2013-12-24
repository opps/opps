#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from opps.containers.models import Container
from opps.channels.models import Channel
from opps.fields.models import Field, Option, FieldOption, FIELD_TYPE


class FieldModelTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.channel = Channel.objects.create(name=u'Home', slug=u'home',
                                              description=u'home page',
                                              site=self.site, user=self.user)

        self.container = Container.objects.create(title=u'test',
                                                  user=self.user,
                                                  published=True,
                                                  site=self.site,
                                                  channel=self.channel)


class FieldFields(TestCase):

    def test_name(self):
        field = Field._meta.get_field_by_name('name')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 100)

    def test_slug(self):
        field = Field._meta.get_field_by_name('slug')[0]
        self.assertEqual(field.__class__, models.SlugField)
        self.assertEqual(field.max_length, 255)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)

    def test_application(self):
        field = Field._meta.get_field_by_name('application')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertTrue(field.db_index)

    def test_type(self):
        field = Field._meta.get_field_by_name('type')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 15)
        self.assertTrue(field.db_index)
        self.assertTrue(field.choices, FIELD_TYPE)


class OptionFields(TestCase):

    def test_field(self):
        field = Option._meta.get_field_by_name('field')[0]
        self.assertEqual(field.__class__, models.ForeignKey)

    def test_name(self):
        field = Field._meta.get_field_by_name('name')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 100)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)

    def test_slug(self):
        field = Option._meta.get_field_by_name('slug')[0]
        self.assertEqual(field.__class__, models.SlugField)
        self.assertEqual(field.max_length, 140)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)

    def test_value(self):
        field = Option._meta.get_field_by_name('value')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)


class FieldOptionFields(TestCase):

    def test_field(self):
        field = FieldOption._meta.get_field_by_name('field')[0]
        self.assertEqual(field.__class__, models.ForeignKey)

    def test_option(self):
        field = FieldOption._meta.get_field_by_name('option')[0]
        self.assertEqual(field.__class__, models.ForeignKey)

    def test_order(self):
        field = FieldOption._meta.get_field_by_name('order')[0]
        self.assertEqual(field.__class__, models.PositiveIntegerField)
        self.assertEqual(field.default, 0)
