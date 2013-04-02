#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.test import TestCase

from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

from opps.sources.models import Source


class SourceModelTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.source = Source.objects.create(name=u'Test site',
                                            slug=u'test-site', user=self.user,
                                            site=self.site)

    def test_check_create_test_site(self):
        """
        Check exist source test site, create on setup class
        """
        source = Source.objects.filter(slug='test-site').get()
        self.assertTrue(source)
        self.assertEqual(source, self.source)

    def test_not_register_url(self):
        """
        url not registered
        """
        source = Source.objects.filter(slug='test-site').get()
        self.assertFalse(self.source.url)
        self.assertEqual(self.source.url, source.url)

    def test_register_url(self):
        """
        url registered
        """
        self.source.url = u"http://example.com/"
        self.source.save()

        source = Source.objects.filter(slug='test-site').get()
        self.assertTrue(self.source.url)
        self.assertEqual(self.source.url, source.url)

    def test_duplicate_source_slug(self):
        """
        create 2 source with same slug
        """
        self.assertRaises(IntegrityError, Source.objects.create,
                          name=u'test site', slug=u'test-site')
