#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.sites.models import Site

from ..models import FlatPage


class FlatPagesFields(TestCase):


    def test_show_in_menu(self):
        field = FlatPage._meta.get_field_by_name('show_in_menu')[0]
        self.assertFalse(field.default)