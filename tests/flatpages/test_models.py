#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models

from opps.flatpages.models import FlatPage


class FlatPagesFields(TestCase):

    def test_show_in_menu(self):
        field = FlatPage._meta.get_field_by_name('show_in_menu')[0]
        self.assertFalse(field.default)

    def test_content(self):
        field = FlatPage._meta.get_field_by_name('content')[0]
        self.assertEqual(field.__class__, models.TextField)

    def test_order(self):
        field = FlatPage._meta.get_field_by_name('order')[0]
        self.assertEqual(field.default, 0)
