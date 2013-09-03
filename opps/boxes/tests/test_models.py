#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models

from ..models import QuerySet, BaseBox


class BoxesFields(TestCase):

    def test_name(self):
        field = QuerySet._meta.get_field_by_name(u"name")[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)

    def test_slug(self):
        field = QuerySet._meta.get_field_by_name(u"slug")[0]
        self.assertEqual(field.__class__, models.SlugField)
        self.assertTrue(field.db_index)
        self.assertEqual(field.max_length, 150)
        self.assertTrue(field.unique)

    def test_model(self):
        field = QuerySet._meta.get_field_by_name(u"model")[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 150)

    def test_limit(self):
        field = QuerySet._meta.get_field_by_name(u"limit")[0]
        self.assertEqual(field.__class__, models.PositiveIntegerField)
        self.assertEqual(field.default, 7)

    def test_order(self):
        field = QuerySet._meta.get_field_by_name(u"order")[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 1)
        self.assertEqual(field.choices, (('-', 'DESC'), ('+', 'ASC')))

    def test_channel(self):
        field = QuerySet._meta.get_field_by_name(u"filters")[0]
        self.assertEqual(field.__class__, models.TextField)
        self.assertEqual(
            field.help_text,
            u"Json format extra filters for queryset"
        )
        self.assertTrue(field.blank)
        self.assertTrue(field.null)


class BaseBoxFields(TestCase):

    def test_name(self):
        field = BaseBox._meta.get_field_by_name(u"name")[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)

    def test_slug(self):
        field = BaseBox._meta.get_field_by_name(u"slug")[0]
        self.assertEqual(field.__class__, models.SlugField)
        self.assertTrue(field.db_index)
        self.assertEqual(field.max_length, 150)
        self.assertTrue(field.unique)
