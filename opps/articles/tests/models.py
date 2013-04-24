#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase

from opps.articles.models import Post


class PostModelTest(TestCase):

    fixtures = ['tests/initial_data.json']

    def setUp(self):
        self.post = Post.objects.get(id=1)

    def test_basic_post_exist(self):
        post = Post.objects.all()

        self.assertTrue(post)
        self.assertTrue(post[0], self.post)
        self.assertEqual(len(post), 1)
        self.assertEqual(post[0].slug, u'test-post-application')
        self.assertEqual(post[0].title, u'test post application')
        self.assertTrue(post[0].short_url)

    def test_child_class(self):

        self.assertTrue(self.post.child_class)
        self.assertEqual(self.post.child_class, 'Post')

    def test_get_absolute_url(self):

        self.assertEqual(self.post.get_absolute_url(),
                         u'/channel-01/test-post-application')
        self.assertEqual(self.post.get_absolute_url(),
                         "/{0}/{1}".format(self.post.channel.long_slug,
                                           self.post.slug))
