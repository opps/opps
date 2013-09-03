#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models

from ..models import Archive


class ArchiveFields(TestCase):

    def test_title(self):
        field = Archive._meta.get_field_by_name(u"title")[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)
        self.assertTrue(field.db_index)

    def test_archive(self):
        field = Archive._meta.get_field_by_name(u"archive")[0]
        self.assertEqual(field.__class__, models.FileField)
        self.assertEqual(field.max_length, 255)

    def test_description(self):
        field = Archive._meta.get_field_by_name(u"description")[0]
        self.assertEqual(field.__class__, models.TextField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_source(self):
        field = Archive._meta.get_field_by_name(u"source")[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
