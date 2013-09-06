#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models

from ..models import Date, Publisher


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
