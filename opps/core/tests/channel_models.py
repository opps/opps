#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

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
        self.assertEqual(home.is_published(), home.published)

    def test_is_published(self):
        """
        is_published true on home channel
        """
        self.channel.published = True
        self.channel.date_available = datetime(2013, 01, 01)
        self.channel.save()

        home = Channel.objects.filter(slug=u'home').get()
        self.assertTrue(home.is_published())
        self.assertEqual(home.is_published(), home.published)

    def test_create_sub_channel_home(self):
        channel = Channel.objects.create(name=u'Sub Home', slug=u'sub-home',
                description=u'sub home page', site=self.site,
                channel=self.channel)

        self.assertTrue(channel)
        self.assertEqual(channel.channel, self.channel)

    def test_not_is_published_sub_channel(self):
        """
        is_published false on home sub channel
        """
        subchannel = Channel.objects.create(name=u'Sub Home', slug=u'sub-home',
                description=u'sub home page', site=self.site,
                channel=self.channel)

        subhome = Channel.objects.filter(slug=u'sub-home').get()
        self.assertFalse(subhome.is_published())
        self.assertEqual(subhome.is_published(), subhome.published)
        self.assertEqual(subhome.is_published(), subchannel.is_published())

    def test_is_published_sub_channel(self):
        """
        is_published true on home sub channel
        """
        subchannel = Channel.objects.create(name=u'Sub Home', slug=u'sub-home',
                description=u'sub home page', site=self.site,
                channel=self.channel)
        subchannel.published = True
        subchannel.date_available = datetime(2013, 01, 01)
        subchannel.save()

        subhome = Channel.objects.filter(slug=u'sub-home').get()
        self.assertTrue(subhome.is_published())
        self.assertEqual(subhome.is_published(), subhome.published)
        self.assertEqual(subhome.is_published(), subhome.is_published())
