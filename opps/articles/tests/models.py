#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.core.files import File

from opps.articles.models import Post
from opps.channels.models import Channel
from opps.images.models import Image


class PostModelTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.channel = Channel.objects.create(name=u'Home', slug=u'home',
                                              description=u'home page',
                                              site=self.site, user=self.user)

        image = File(open("opps/__init__.py"), "test_file.png")
        self.image = Image.objects.create(site=self.site, title='test',
                                          image=image, user=self.user)

        self.post = Post.objects.create(
            title=u'Basic test',
            slug=u'basic-test',
            short_title=u'Write basict test for Article type Post',
            content=u'This field is context',
            main_image=self.image,
            channel=self.channel,
            user=self.user
        )

    def test_basic_post_exist(self):
        post = Post.objects.all()

        self.assertTrue(post)
        self.assertEqual(post[0], self.post)
