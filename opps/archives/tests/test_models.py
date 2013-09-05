#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from django.test import TestCase
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.core.files import File as DjangoFile

from ..models import Archive, File, get_file_path


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


class ArchiveTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.file = File.objects.create(user=self.user, site=self.site,
                                        archive=DjangoFile(
                                            open("README.rst"), "test.png"),
                                        title=u"Test")

    def test_get_file_path(self):
        path = get_file_path(self.file, "test.png")
        d = datetime.now()
        self.assertTrue(path)
        self.assertIn(u"archives/{}".format(d.strftime("%Y/%m/%d/")), path)
        self.assertIn(self.file.slug[:100], path)
