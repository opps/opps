#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone

from opps.articles.models import Post, Link
from opps.channels.models import Channel


class TemplateNameTest(TestCase):

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
        self.post = Post.objects.create(
            headline=u'a simple headline',
            short_title=u'a simple short title',
            title=u'a simple title',
            hat=u'a simple hat',
            channel=self.channel,
            user=self.user,
            published=True,
            date_available=timezone.now(),
        )

    def test_get_template_name_basic(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertTrue(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            ['containers/test-channel/a-simple-title/detail.html',
             'containers/test-channel/post_detail.html',
             'containers/post_detail.html',
             'containers/test-channel/detail.html',
             'containers/detail.html'])

    def test_get_template_name_channel_with_father(self):
        channel = Channel.objects.create(
            name='child',
            slug='child',
            parent=self.channel,
            user=self.user,
            published=True,
            date_available=timezone.now(),
        )
        self.post.channel = channel
        self.post.save()

        response = self.client.get(self.post.get_absolute_url())
        self.assertTrue(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            ['containers/test-channel/child/a-simple-title/detail.html',
             'containers/test-channel/child/post_detail.html',
             'containers/test-channel/post_detail.html',
             'containers/post_detail.html',
             'containers/test-channel/child/detail.html',
             'containers/test-channel/detail.html',
             'containers/detail.html'])


class LinkResponseToRedirecTest(TestCase):

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
        self.link = Link.objects.create(
            title=u'a simple title',
            url=u'http://www.oppsproject.org/',
            channel=self.channel,
            user=self.user,
            published=True,
            date_available=timezone.now(),
        )

    def test_redirect(self):
        response = self.client.get(self.link.get_absolute_url())
        self.assertTrue(response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.items()[2][1],
                         u'http://www.oppsproject.org/')
