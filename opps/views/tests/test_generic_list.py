#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone

from opps.articles.models import Post, Link
from opps.channels.models import Channel


class TestTemplateName(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='test@test.com',
            email='test@test.com',
            password=User.objects.make_random_password(),
        )
        self.channel = Channel.objects.create(
            name='test channel',
            slug='test-channel',
            user=self.user,
            published=True,
            date_available=timezone.now(),
        )

    def test_get_template_name_basic(self):
        response = self.client.get(self.channel.get_absolute_url())
        self.assertTrue(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            ['containers/test-channel/list.html',
             'containers/list.html'])

    def test_get_template_name_subchannel(self):
        channel = Channel.objects.create(
            name='test subchannel',
            slug='test-subchannel',
            parent=self.channel,
            user=self.user,
            published=True,
            date_available=timezone.now(),
        )

        response = self.client.get(channel.get_absolute_url())
        self.assertTrue(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            ['containers/test-channel/test-subchannel/list.html',
             'containers/test-channel/list.html',
             'containers/list.html'])

    """
    def test_querystring_page_is_2(self):
        response = self.client.get("{}?page=2".format(self.channel.get_absolute_url()))
        self.assertTrue(response)
        import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            ['containers/test-channel/list.html',
             'containers/list.html'])
    """
