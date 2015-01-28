# -*- coding: utf-8 -*-
from django.test import TestCase

from opps.fields.utils import field_template_read


class FieldTemplateReadlTest(TestCase):

    def setUp(self):
        self.dict = {"articlespost-checkbox-show-main-image_yes": "1"}
        self.dict_out = {"articlespost_checkbox_show_main_image_yes": "1"}

    def test_self_dict(self):
        read_on_template = field_template_read(self.dict)

        self.assertNotEqual(self.dict, self.dict_out)
        self.assertTrue(read_on_template)
        self.assertEqual(read_on_template, self.dict_out)

    def test_empty_dict(self):
        """Dict empty is false in Python"""
        read_on_template = field_template_read({})
        self.assertFalse(read_on_template)
        self.assertEqual(read_on_template, {})

    def test_down_case(self):
        read_on_template = field_template_read(self.dict_out)
        self.assertEqual(read_on_template, self.dict_out)
