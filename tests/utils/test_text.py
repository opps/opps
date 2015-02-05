#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from opps.utils.text import split_tags


class SplitTags(TestCase):
    def test_common(self):
        source = 'gabriela pugliesi e Ricardo,NOVIDADE,instagram'
        output = ['gabriela pugliesi e Ricardo', 'NOVIDADE', 'instagram']
        self.assertEqual(split_tags(source), output)

    def test_duplicated_comma(self):
        source = 'entretenimento,,Taylor Swift,The Voice,famosos'
        output = ['entretenimento', 'Taylor Swift', 'The Voice', 'famosos']
        self.assertEqual(split_tags(source), output)

    def test_duplicated_commas_and_extra_spaces(self):
        source = ',entretenimento,,    Taylor Swift,  The Voice,famosos  , ,'
        output = ['entretenimento', 'Taylor Swift', 'The Voice', 'famosos']
        self.assertEqual(split_tags(source), output)

    def test_another_separator(self):
        source = 'Mariah Carey{0}filhos{0}música{0}entretenimento'
        output = ['Mariah Carey', 'filhos', 'música', 'entretenimento']
        self.assertEqual(split_tags(source.format('|'), separator="|"), output)
        self.assertEqual(split_tags(source.format('#'), separator="#"), output)

        # Multiple chars
        self.assertEqual(split_tags(source.format('%%'), separator="%%"),
                         output)

    def test_empty(self):
        self.assertEqual(split_tags(' '), [])
        self.assertEqual(split_tags('   '), [])
