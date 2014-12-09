# -*- encoding: utf-8 -*-
import string
import random

from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User

from opps.articles.models import Article, Post, Album
from opps.articles.models import PostRelated, Link
from opps.channels.models import Channel

from opps.core.tags.models import Tag
from opps.core.managers import PublishableManager


class ArticleFields(TestCase):

    def test_headline(self):
        field = Article._meta.get_field_by_name('headline')[0]
        self.assertEqual(field.__class__, models.TextField)

    def test_short_title(self):
        field = Article._meta.get_field_by_name('short_title')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)


class PostFields(TestCase):

    def test_content(self):
        field = Post._meta.get_field_by_name('content')[0]
        self.assertEqual(field.__class__, models.TextField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)

    def test_albums(self):
        field = Post._meta.get_field_by_name('albums')[0]
        self.assertEqual(field.__class__, models.ManyToManyField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_related_containers(self):
        field = Post._meta.get_field_by_name('related_containers')[0]
        self.assertEqual(field.__class__, models.ManyToManyField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)


class PostRelatedFields(TestCase):

    def test_post(self):
        field = PostRelated._meta.get_field_by_name(u"post")[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_related(self):
        field = PostRelated._meta.get_field_by_name(u"related")[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)


class LinkFields(TestCase):

    def test_url(self):
        field = Link._meta.get_field_by_name(u"url")[0]
        self.assertEqual(field.__class__, models.URLField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)


class PostCreation(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test@test.com',
            email='test@test.com',
            password=User.objects.make_random_password(),
        )

        self.channel = Channel.objects.create(
            name='test channel',
            user=self.user,
        )

        self.post = Post.objects.create(
            headline=u'a simple headline',
            short_title=u'a simple short title',
            title=u'a simple title',
            hat=u'a simple hat',
            channel=self.channel,
            user=self.user,
        )

    def test_post_fields(self):
        self.assertTrue(self.post.headline, u'a simple headline')
        self.assertTrue(self.post.short_title, u'a simple short title')
        self.assertTrue(self.post.title, u'a simple title')
        self.assertTrue(self.post.hat, u'a simple hat')
        self.assertTrue(self.post.channel, self.channel)
        self.assertTrue(self.post.user, self.user)

    def test_multiple_tags_in_post(self):
        self.post.tags = u','.join(self._gen_tags(100))
        self.post.save()
        self.assertEqual(Tag.objects.count(), 100)

    def test_raiser_tags(self):
        self.post.tags = u"opps, cms, , post"
        self.post.save()
        self.assertEqual([t.name for t in self.post.get_tags()],
                         ['opps', 'cms', 'post'])

    def test_ordered_tags(self):
        self.post.tags = u"zyx,opps,cms,opps,post"
        self.post.save()
        self.assertEqual([t.name for t in self.post.get_tags()],
                         [u'zyx', u'opps', u'cms', u'post'])

    def _gen_tags(self, length):
        tags = []
        for i in range(length):
            tag = u''.join(random.choice(string.ascii_uppercase)
                           for x in range(12))
            tags.append(tag)
        return tags


class LinkCreation(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test@test.com',
            email='test@test.com',
            password=User.objects.make_random_password(),
        )
        self.channel = Channel.objects.create(
            name='test channel',
            user=self.user,
        )
        self.link = Link.objects.create(
            user=self.user,
            channel=self.channel,
            url='http://www.google.com',
            headline=u'a beatiful headline',
            short_title=u'a simple short title',
            title=u'a simple title',
            hat=u'a simple hat',
        )

    def test_link_fields(self):
        self.assertTrue(self.link.url, u'http://www.google.com')
        self.assertTrue(self.link.channel, self.channel)
        self.assertTrue(self.link.user, self.user)
        self.assertTrue(self.link.short_title, u'a simple short title')
        self.assertTrue(self.link.title, u'a simple title')
        self.assertTrue(self.link.hat, u'a simple hat')

    def test_is_local(self):
        self.assertFalse(self.link.is_local())

    def test_is_subdomain(self):
        self.assertFalse(self.link.is_subdomain())


class AlbumCreation(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test@test.com',
            email='test@test.com',
            password=User.objects.make_random_password(),
        )
        self.channel = Channel.objects.create(
            name='test channel',
            user=self.user,
        )
        self.album = Album.objects.create(
            user=self.user,
            channel=self.channel,
            headline=u'a beatiful headline',
            short_title=u'a simple short title',
            title=u'a simple title',
            hat=u'a simple hat',
        )

    def test_album_fields(self):
        self.assertTrue(self.album.channel, self.channel)
        self.assertTrue(self.album.user, self.user)
        self.assertTrue(self.album.short_title, u'a simple short title')
        self.assertTrue(self.album.title, u'a simple title')
        self.assertTrue(self.album.hat, u'a simple hat')


class PostPublishableManager(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test@test.com',
            email='test@test.com',
            password=User.objects.make_random_password(),
        )

        self.channel = Channel.objects.create(
            name='test channel',
            user=self.user,
        )

        self.post = Post.objects.create(
            headline=u'a simple headline',
            short_title=u'a simple short title',
            title=u'a simple title',
            hat=u'a simple hat',
            channel=self.channel,
            user=self.user,
        )

        from django.db.models import Model

        class ModelYet(Model):
            objects = PublishableManager()
        self.Model = ModelYet

    def test_custom_manager(self):
        self.assertEquals(Post.objects.all_published().count(), 0)

        self.post.published = True
        self.post.save()

        self.assertEquals(Post.objects.all_published().count(), 1)
