#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.test import TestCase

from opps.core.models.source import Source


class SourceModelTest(TestCase):

    def setUp(self):
        self.source = Source.objects.create(name=u'Test site',
                slug=u'test-site')

