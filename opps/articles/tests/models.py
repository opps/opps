#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase

from opps.articles.models import Post


class PostModelTest(TestCase):

    fixtures = ['tests/initial_data.json']

    def test_basic_post_exist(self):
        post = Post.objects.all()

        self.assertTrue(post)
        self.assertEqual(len(post), 1)
        self.assertEqual(post[0].slug, u'test-post-application')
        self.assertEqual(post[0].title, u'test post application')
        self.assertTrue(post[0].short_url)
