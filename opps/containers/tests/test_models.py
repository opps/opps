#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from ..models import Container
from opps.channels.models import Channel


class ContainerFields(TestCase):

    def test_title(self):
        field = Container._meta.get_field_by_name('title')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)
        self.assertTrue(field.db_index)

    def test_hat(self):
        field = Container._meta.get_field_by_name('hat')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_short_url(self):
        field = Container._meta.get_field_by_name('short_url')[0]
        self.assertEqual(field.__class__, models.URLField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_child_class(self):
        field = Container._meta.get_field_by_name('child_class')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 30)
        self.assertTrue(field.db_index)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_child_module(self):
        field = Container._meta.get_field_by_name('child_module')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 120)
        self.assertTrue(field.db_index)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_child_app_label(self):
        field = Container._meta.get_field_by_name('child_app_label')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 30)
        self.assertTrue(field.db_index)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_show_on_root_channel(self):
        field = Container._meta.get_field_by_name('show_on_root_channel')[0]
        self.assertEqual(field.__class__, models.BooleanField)
        self.assertTrue(field.default)

    def test_sourcesl(self):
        field = Container._meta.get_field_by_name('sources')[0]
        self.assertEqual(field.__class__, models.ManyToManyField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertFalse(field.unique)
        self.assertFalse(field.primary_key)


class ContainerModelTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.channel = Channel.objects.create(name=u'Home', slug=u'home',
                                              description=u'home page',
                                              site=self.site, user=self.user)

        self.container = Container.objects.create(title=u'test',
                                                  user=self.user,
                                                  site=self.site,
                                                  channel=self.channel)

    def test_with_containers_exists(self):
        self.assertTrue(self.container)
        self.assertEqual(self.container.title, u'test')
        container = Container.objects.get(title=u'test')
        self.assertEqual(container, self.container)

    def test_save_with_test_desnomalization(self):
        self.assertEqual(self.container.channel_name, self.channel.name)
        self.assertEqual(self.container.channel_long_slug,
                         self.channel.long_slug)
        self.assertEqual(self.container.child_class, u"Container")
        self.assertEqual(self.container.child_module,
                         u"opps.containers.models")
        self.assertEqual(self.container.child_app_label, u"containers")

    def test_absolute_url(self):
        self.assertEqual(self.container.get_absolute_url(),
                         u"/home/test")
