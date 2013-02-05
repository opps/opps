#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.sites.models import Site

from opps.core.models.channel import Channel


class ChannelModelTest(TestCase):

    def setUp(self):
        self.site = Site.objects.filter(name=u'example.com').get()
        self.channel = Channel.objects.create(name=u'Home', slug=u'home',
                description=u'home page', site=self.site)

