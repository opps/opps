#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from django.db import IntegrityError
from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils import timezone

from opps.channels.models import Channel


class ChannelModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.parent = Channel.objects.create(name=u'Home', slug=u'home',
                                             description=u'home page',
                                             site=self.site, user=self.user)

    def test_check_create_home(self):
        """
        Check exist channel home, create on setup class
        """
        home = Channel.objects.filter(slug=u'home').get()
        self.assertTrue(home)
        self.assertEqual(home, self.parent)

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
        self.parent.published = True
        self.parent.date_available = timezone.now() - timedelta(hours=1)
        self.parent.save()

        home = Channel.objects.filter(slug=u'home').get()
        self.assertTrue(home.is_published())
        self.assertEqual(home.is_published(), home.published)

    def test_create_sub_channel_home(self):
        channel = Channel.objects.create(name=u'Sub Home', slug=u'sub-home',
                                         description=u'sub home page',
                                         site=self.site, parent=self.parent,
                                         user=self.user)

        self.assertTrue(channel)
        self.assertEqual(channel.parent, self.parent)

    def test_not_is_published_sub_channel(self):
        """
        is_published false on home sub channel
        """
        subchannel = Channel.objects.create(name=u'Sub Home', slug=u'sub-home',
                                            description=u'sub home page',
                                            site=self.site, user=self.user,
                                            parent=self.parent)

        subhome = Channel.objects.filter(slug=u'sub-home').get()
        self.assertFalse(subhome.is_published())
        self.assertEqual(subhome.is_published(), subhome.published)
        self.assertEqual(subhome.is_published(), subchannel.is_published())

    def test_is_published_sub_channel(self):
        """
        is_published true on home sub channel
        """
        subchannel = Channel.objects.create(name=u'Sub Home', slug=u'sub-home',
                                            description=u'sub home page',
                                            site=self.site, user=self.user,
                                            parent=self.parent)
        subchannel.published = True
        subchannel.date_available = timezone.now() - timedelta(hours=1)
        subchannel.save()

        subhome = Channel.objects.filter(slug=u'sub-home').get()
        self.assertTrue(subhome.is_published())
        self.assertEqual(subhome.is_published(), subhome.published)
        self.assertEqual(subhome.is_published(), subhome.is_published())

    def test_duplicate_channel_name(self):
        """
        create 2 channel with same name
        """
        Channel.objects.create(name=u'Sub Home', slug=u'sub-home',
                               description=u'sub home page', site=self.site,
                               parent=self.parent, user=self.user)

        self.assertRaises(IntegrityError, Channel.objects.create,
                          name=u'Sub Home', slug=u'sub-home',
                          description=u'sub home page', site=self.site,
                          parent=self.parent)

    def test_channel_is_homepage(self):
        """
        check channel is home page
        """
        self.parent.homepage = True
        self.parent.published = True
        self.parent.save()

        channel = Channel.objects.get_homepage(site=self.parent.site)
        self.assertTrue(channel)
        self.assertEqual(channel.slug, self.parent.slug)

    def test_not_set_homeoage(self):
        """
        not set channel home page, return none
        """

        channel = Channel.objects.get_homepage(site=self.parent.site)
        self.assertEqual(None, channel)
        self.assertFalse(channel)
