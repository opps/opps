#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from opps.containers.models import Container
from opps.containers.models import ContainerImage, ContainerBox
from opps.containers.models import ContainerBoxContainers, Mirror
from opps.containers.tasks import check_mirror_channel
from opps.channels.models import Channel


class ContainerModelTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.channel = Channel.objects.create(name=u'Home', slug=u'home',
                                              description=u'home page',
                                              site=self.site, user=self.user)

        self.container = Container.objects.create(title=u'test',
                                                  user=self.user,
                                                  published=True,
                                                  site=self.site,
                                                  channel=self.channel)

    def test_with_containers_exists(self):
        self.assertTrue(self.container)
        self.assertEqual(self.container.title, u'test')
        container = Container.objects.get(title=u'test')
        self.assertEqual(container, self.container)

    def test_save_with_test_desnomalization(self):
        self.assertEqual(self.container.channel_name, self.channel.name)
        self.assertEqual(self.container.channel_long_slug,
                         self.channel.long_slug)
        self.assertEqual(self.container.child_class, u"Container")
        self.assertEqual(self.container.child_module,
                         u"opps.containers.models")
        self.assertEqual(self.container.child_app_label, u"containers")

    def test_absolute_url(self):
        self.assertEqual(self.container.get_absolute_url(),
                         u"/home/test.html")

    def test_get_thumb(self):
        self.assertFalse(self.container.get_thumb())

    def test_search_category(self):
        self.assertEqual(self.container.search_category, u"Container")

    def test_get_http_absolute_url(self):
        self.assertEqual(self.container.get_http_absolute_url(),
                         u'http://example.com/home/test.html')

    def test_create_channel_mirror(self):
        channel = Channel.objects.create(name=u'Home2', slug=u'home2',
                                         description=u'home page2',
                                         site=self.site, user=self.user)
        self.container.mirror_channel.add(channel)
        self.container.save()
        check_mirror_channel(self.container, Mirror)
        mirror = Mirror.objects.all()

        self.assertTrue(mirror)
        self.assertEqual(len(mirror), 1)
        self.assertEqual(mirror[0].get_absolute_url(), u"/home2/test.html")
        self.assertEqual(len(Container.objects.all()), 2)

    def test_remove_channel_mirror(self):
        channel = Channel.objects.create(name=u'Home2', slug=u'home2',
                                         description=u'home page2',
                                         site=self.site, user=self.user)
        self.container.mirror_channel.add(channel)
        self.container.save()
        check_mirror_channel(self.container, Mirror)
        self.container.mirror_channel.remove(channel)
        self.container.save()
        check_mirror_channel(self.container, Mirror)
        mirror = Mirror.objects.all()

        self.assertFalse(mirror)
        self.assertEqual(len(mirror), 0)


class ContainerFields(TestCase):

    def test_title(self):
        field = Container._meta.get_field_by_name('title')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)
        self.assertTrue(field.db_index)

    def test_hat(self):
        field = Container._meta.get_field_by_name('hat')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_short_url(self):
        field = Container._meta.get_field_by_name('short_url')[0]
        self.assertEqual(field.__class__, models.URLField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_child_class(self):
        field = Container._meta.get_field_by_name('child_class')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 30)
        self.assertTrue(field.db_index)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_child_module(self):
        field = Container._meta.get_field_by_name('child_module')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 120)
        self.assertTrue(field.db_index)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_child_app_label(self):
        field = Container._meta.get_field_by_name('child_app_label')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 30)
        self.assertTrue(field.db_index)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_show_on_root_channel(self):
        field = Container._meta.get_field_by_name('show_on_root_channel')[0]
        self.assertEqual(field.__class__, models.BooleanField)
        self.assertTrue(field.default)

    def test_source(self):
        field = Container._meta.get_field_by_name('source')[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)


class ContainerImageFields(TestCase):

    def test_container(self):
        field = ContainerImage._meta.get_field_by_name(u"container")[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.verbose_name, u"Container")

    def test_order(self):
        field = ContainerImage._meta.get_field_by_name(u"order")[0]
        self.assertEqual(field.__class__, models.PositiveIntegerField)
        self.assertEqual(field.default, 0)

    def test_image(self):
        field = ContainerImage._meta.get_field_by_name(u"image")[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.verbose_name, u"Image")

    def test_caption(self):
        field = ContainerImage._meta.get_field_by_name(u"caption")[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)


class ContainerBoxFields(TestCase):

    def test_title(self):
        field = ContainerBox._meta.get_field_by_name(u"title")[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.max_length, 140)

    def test_containers(self):
        field = ContainerBox._meta.get_field_by_name(u"containers")[0]
        self.assertEqual(field.__class__, models.ManyToManyField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.verbose_name, u"Container")

    def test_queryset(self):
        field = ContainerBox._meta.get_field_by_name(u"queryset")[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.verbose_name, u"Query Set")


class ContainerBoxContainersFields(TestCase):

    def test_containerbox(self):
        field = ContainerBoxContainers._meta.get_field_by_name(
            u"containerbox"
        )[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.verbose_name, u"Container Box")

    def test_container(self):
        field = ContainerBoxContainers._meta.get_field_by_name(u"container")[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.verbose_name, u"Container")

    def test_order(self):
        field = ContainerBoxContainers._meta.get_field_by_name(u"order")[0]
        self.assertEqual(field.__class__, models.PositiveIntegerField)
        self.assertEqual(field.default, 0)

    def test_aggregate(self):
        field = ContainerBoxContainers._meta.get_field_by_name(
            u"aggregate"
        )[0]
        self.assertEqual(field.default, 0)

    def test_date_available(self):
        field = ContainerBoxContainers._meta.get_field_by_name(
            u"date_available"
        )[0]
        self.assertEqual(field.__class__, models.DateTimeField)
        self.assertTrue(field.null)

    def test_date_end(self):
        field = ContainerBoxContainers._meta.get_field_by_name(u"date_end")[0]
        self.assertEqual(field.__class__, models.DateTimeField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_title(self):
        field = ContainerBoxContainers._meta.get_field_by_name(u"title")[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_hat(self):
        field = ContainerBoxContainers._meta.get_field_by_name(
            u"hat"
        )[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_url(self):
        field = ContainerBoxContainers._meta.get_field_by_name(
            u"url"
        )[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_main_image(self):
        field = ContainerBoxContainers._meta.get_field_by_name(
            u"main_image"
        )[0]
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.verbose_name, u"Main Image")

    def test_main_image_caption(self):
        field = ContainerBoxContainers._meta.get_field_by_name(
            u"main_image_caption"
        )[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 4000)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.help_text, u"Maximum characters 4000")
