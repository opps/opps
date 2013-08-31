#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models

from ..models import Date


class DateFields(TestCase):

    def test_date_insert(self):
        field = Date._meta.get_field_by_name('date_insert')[0]
        self.assertEqual(field.__class__, models.DateTimeField)
        self.assertTrue(field.auto_now_add)

    def test_date_update(self):
        field = Date._meta.get_field_by_name('date_update')[0]
        self.assertEqual(field.__class__, models.DateTimeField)
        self.assertTrue(field.auto_now)
