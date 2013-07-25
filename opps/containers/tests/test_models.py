#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models

#from taggit.managers import TaggableManager
from opps.core.tags.fields import TagField
from ..models import Container


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

    def test_tags(self):
        field = Container._meta.get_field_by_name('tags')[0]
        self.assertEqual(field.__class__, TagField)
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
