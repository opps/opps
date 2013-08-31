#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

from opps.channels.models import Channel
from opps.core.widgets import OppsEditor

from ..models import Post
from ..forms import PostAdminForm


class PostAdminFormTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.channel = Channel.objects.create(name=u'Home', slug=u'home',
                                              description=u'home page',
                                              site=self.site, user=self.user)

    def test_init(self):
        """
        Test successful init without data
        """
        self.post = Post.objects.create(title=u'test', user=self.user,
                                        site=self.site, channel=self.channel)
        form = PostAdminForm(instance=self.post)
        self.assertTrue(isinstance(form.instance, Post))
        self.assertEqual(form.instance.pk, self.post.pk)

    def test_default_multiupload_link(self):
        """
        Test default value field multiupload link
        """
        self.post = Post.objects.create(title=u'test', user=self.user,
                                        site=self.site, channel=self.channel)
        form = PostAdminForm(instance=self.post)
        self.assertEqual(form.multiupload_link, '/fileupload/image/')

    def test_editor_widgets(self):
        """
        Test auto set field widget Editor
        """
        self.post = Post.objects.create(title=u'test', user=self.user,
                                        site=self.site, channel=self.channel)
        form = PostAdminForm(instance=self.post)
        self.assertTrue(isinstance(form.fields['content'].widget,
                                   OppsEditor))
