#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import timedelta
from mptt.models import TreeForeignKey

from django.db import IntegrityError
from django.test import TestCase
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from opps.channels.models import Channel


class ChannelFields(TestCase):

    def test_name(self):
        field = Channel._meta.get_field_by_name('name')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 60)

    def test_long_slug(self):
        field = Channel._meta.get_field_by_name('long_slug')[0]
        self.assertEqual(field.__class__, models.SlugField)
        self.assertEqual(field.max_length, 250)
        self.assertTrue(field.db_index)

    def test_layout(self):
        field = Channel._meta.get_field_by_name('layout')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 250)
        self.assertTrue(field.db_index)
        self.assertEqual(field.default, u"default")

    def test_description(self):
        field = Channel._meta.get_field_by_name('description')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_show_in_menu(self):
        field = Channel._meta.get_field_by_name('show_in_menu')[0]
        self.assertEqual(field.__class__, models.BooleanField)
        self.assertFalse(field.default)

    def test_include_in_main_rss(self):
        field = Channel._meta.get_field_by_name('include_in_main_rss')[0]
        self.assertEqual(field.__class__, models.BooleanField)
        self.assertTrue(field.default)

    def test_homepage(self):
        field = Channel._meta.get_field_by_name('homepage')[0]
        self.assertEqual(field.__class__, models.BooleanField)
        self.assertFalse(field.default)
        self.assertEqual(field.help_text,
                         u'Check only if this channel is the homepage.'
                         u' Should have only one homepage per site')

    def test_group(self):
        field = Channel._meta.get_field_by_name('group')[0]
        self.assertEqual(field.__class__, models.BooleanField)
        self.assertFalse(field.default)

    def test_order(self):
        field = Channel._meta.get_field_by_name('order')[0]
        self.assertEqual(field.__class__, models.IntegerField)
        self.assertEqual(field.default, 0)

    def test_parent(self):
        field = Channel._meta.get_field_by_name('parent')[0]
        self.assertEqual(field.__class__, TreeForeignKey)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)


class ChannelModelTest(TestCase):

    def setUp(self):
        User = get_user_model()
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

    def test_not_set_homepage(self):
        """
        not set channel home page, return none
        """

        channel = Channel.objects.get_homepage(site=self.parent.site)
        self.assertEqual(None, channel)
        self.assertFalse(channel)

    def test_get_thumb(self):
        self.assertIsNone(self.parent.get_thumb())

    def test_search_category(self):
        self.assertEqual(_(u'Channel'), Channel().search_category)

    def test_title(self):
        self.assertEqual(self.parent.title, self.parent.name)

    def test_root(self):
        self.assertEqual(self.parent, self.parent.root)
        subchannel = Channel.objects.create(name=u'Sub Home', slug=u'sub-home',
                                            description=u'sub home page',
                                            site=self.site, user=self.user,
                                            parent=self.parent)
        self.assertEqual(self.parent, subchannel.root)

    def test_clean_slug_exist_in_domain(self):
        invalid = Channel(name=u'Home', slug=u'home', description=u'home page',
                          site=self.site, user=self.user)
        self.assertRaises(ValidationError, invalid.full_clean)

    def test_clean_slug_exist_homepage(self):
        Channel.objects.create(name=u'homepage', slug=u'homepage',
                               homepage=True, site=self.site,
                               user=self.user, published=True)
        invalid = Channel.objects.create(name=u'invalid', slug=u'invalid',
                                         homepage=True, site=self.site,
                                         user=self.user)
        self.assertRaises(ValidationError, invalid.full_clean)

    def test_clean(self):
        valid = Channel.objects.create(name=u'homepage', slug=u'homepage',
                                       homepage=True, site=self.site,
                                       user=self.user, published=True)
        valid.full_clean()

    def test_long_slug(self):
        channel1 = Channel.objects.create(name=u'Channel 1', slug=u'channel1',
                                          parent=self.parent,
                                          description=u'channel 1',
                                          site=self.site, user=self.user)
        channel2 = Channel.objects.create(name=u'Channel 2', slug=u'channel2',
                                          parent=channel1,
                                          description=u'channel 2',
                                          site=self.site, user=self.user)
        self.assertEqual(self.parent.long_slug, 'home')
        self.assertEqual(channel1.long_slug, 'home/channel1')
        self.assertEqual(channel2.long_slug, 'home/channel1/channel2')

    def test_unicode(self):
        channel1 = Channel.objects.create(name=u'Channel 1', slug=u'channel1',
                                          parent=self.parent,
                                          description=u'channel 1',
                                          site=self.site, user=self.user)
        channel2 = Channel.objects.create(name=u'Channel 2', slug=u'channel2',
                                          parent=channel1,
                                          description=u'channel 2',
                                          site=self.site, user=self.user)
        self.assertEqual(self.parent.__unicode__(), '/home/')
        self.assertEqual(channel1.__unicode__(), '/home/channel1/')
        self.assertEqual(channel2.__unicode__(), '/home/channel1/channel2/')

    def test_get_absolute_url(self):
        self.test_unicode()
