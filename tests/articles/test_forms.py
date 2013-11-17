#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

from opps.channels.models import Channel
from opps.core.widgets import OppsEditor

from opps.articles.models import Post, Album
from opps.articles.forms import PostAdminForm, AlbumAdminForm


class PostAdminFormTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.channel = Channel.objects.create(name=u'Home', slug=u'home',
                                              description=u'home page',
                                              site=self.site, user=self.user)
        self.post = Post.objects.create(title=u'test', user=self.user,
                                        site=self.site, channel=self.channel)

    def test_init(self):
        """
        Test successful init without data
        """
        form = PostAdminForm(instance=self.post)
        self.assertTrue(isinstance(form.instance, Post))
        self.assertEqual(form.instance.pk, self.post.pk)

    def test_default_multiupload_link(self):
        """
        Test default value field multiupload link
        """
        form = PostAdminForm(instance=self.post)
        self.assertEqual(form.multiupload_link, '/fileupload/image/')

    def test_editor_widgets(self):
        """
        Test auto set field widget Editor
        """
        form = PostAdminForm(instance=self.post)
        self.assertTrue(isinstance(form.fields['content'].widget,
                                   OppsEditor))


class AlbumAdminFormTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.channel = Channel.objects.create(name=u'Home', slug=u'home',
                                              description=u'home page',
                                              site=self.site, user=self.user)
        self.album = Album.objects.create(title=u'test', user=self.user,
                                          site=self.site, channel=self.channel)

    def test_init(self):
        """
        Test successful init without data
        """
        form = AlbumAdminForm(instance=self.album)
        self.assertTrue(isinstance(form.instance, Album))
        self.assertEqual(form.instance.pk, self.album.pk)

    def test_default_multiupload_link(self):
        """
        Test default value field multiupload link
        """
        form = AlbumAdminForm(instance=self.album)
        self.assertEqual(form.multiupload_link, '/fileupload/image/')

    def test_editor_widgets(self):
        """
        Test auto set field widget Editor
        """
        form = AlbumAdminForm(instance=self.album)
        self.assertTrue(isinstance(form.fields['headline'].widget,
                                   OppsEditor))
