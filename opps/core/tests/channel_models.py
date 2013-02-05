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

    def test_check_create_home(self):
        """
        Check exist channel home, create on setup class
        """
        home = Channel.objects.filter(slug=u'home').get()
        self.assertTrue(home)
        self.assertEqual(home, self.channel)

    def test_not_is_published(self):
        """
        is_published false on home channel
        """
        home = Channel.objects.filter(slug=u'home').get()
        self.assertFalse(home.is_published())
