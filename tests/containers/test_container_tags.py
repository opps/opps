#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.utils import timezone

from opps.containers.models import Container
from opps.channels.models import Channel

from opps.containers.templatetags.container_tags import \
    get_containers_by, get_container_by_channel, filter_queryset_by, \
    exclude_queryset_by


class ExcludeQuerysetByTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username=u'test', password='test')
        site = Site.objects.filter(name=u'example.com').get()
        channel = Channel.objects.create(name=u'Home', slug=u'home',
                                         description=u'home page',
                                         site=site, user=user)

        Container.objects.create(title=u'test',
                                 user=user,
                                 published=True,
                                 site=site,
                                 channel=channel)
        Container.objects.create(title=u'test 2',
                                 user=user,
                                 site=site,
                                 channel=channel)

    def test_tag(self):
        container = Container.objects.all()
        exclude = exclude_queryset_by(container, published=True)
        self.assertTrue(exclude)
        self.assertEqual(len(container), 2)
        self.assertEqual(len(exclude), 1)


class FilterQuerysetByTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username=u'test', password='test')
        site = Site.objects.filter(name=u'example.com').get()
        channel = Channel.objects.create(name=u'Home', slug=u'home',
                                         description=u'home page',
                                         site=site, user=user)

        Container.objects.create(title=u'test',
                                 user=user,
                                 published=True,
                                 site=site,
                                 channel=channel)
        Container.objects.create(title=u'test 2',
                                 user=user,
                                 site=site,
                                 channel=channel)

    def test_tag(self):
        container = Container.objects.all()
        filter1 = filter_queryset_by(container, published=True)
        self.assertTrue(filter1)
        self.assertEqual(len(container), 2)
        self.assertEqual(len(filter1), 1)


class GetContainerByTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username=u'test', password='test')
        site = Site.objects.filter(name=u'example.com').get()
        channel = Channel.objects.create(name=u'Home', slug=u'home',
                                         description=u'home page',
                                         site=site, user=user)

        self.container = Container.objects.create(title=u'test',
                                                  user=user,
                                                  published=True,
                                                  site=site,
                                                  channel=channel)

    def test_tag(self):
        container = get_containers_by(title=u'test')
        self.assertTrue(container)
        self.assertEqual(container[0], self.container)
        self.assertEqual(len(container), 1)

    def test_more_filter(self):
        container = get_containers_by(title=u'test',
                                      user__username=u'test')
        self.assertTrue(container)
        self.assertEqual(container[0].id, 1)
        self.assertEqual(container[0].user.username, u'test')


class GetContainerByChannelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.channel = Channel.objects.create(name=u'Home', slug=u'home',
                                              description=u'home page',
                                              site=self.site, user=self.user)
        self.channel2 = Channel.objects.create(
            name=u'Home2', slug=u'home2',
            description=u'home page2',
            site=self.site, user=self.user)

        self.channel3 = Channel.objects.create(
            name=u'Home3', slug=u'home3',
            description=u'home page3',
            parent=self.channel2,
            site=self.site, user=self.user)

        self.count_container_create = [1, 2, 3, 4, 5]

        for i in self.count_container_create:
            Container.objects.create(title=u'test {0}'.format(i),
                                     user=self.user,
                                     published=True,
                                     site=self.site,
                                     channel=self.channel)
        Container.objects.create(title=u'test channel 2',
                                 user=self.user,
                                 published=True,
                                 site=self.site,
                                 channel=self.channel2)

    def test_tag_one_channel(self):
        get_container = get_container_by_channel('home')
        self.assertEqual(len(get_container), len(self.count_container_create))
        for c, i in zip(self.count_container_create[::-1], get_container):
            self.assertEqual(i.slug, "test-{0}".format(c))

    def test_tag_another_channel(self):
        get_container = get_container_by_channel('home2')
        self.assertEqual(len(get_container), 1)
        self.assertEqual(get_container[0].slug, "test-channel-2")

    def test_get_container_recursive(self):
        for i in self.count_container_create:
            Container.objects.create(title=u'test 3 {0}'.format(i),
                                     user=self.user,
                                     published=True,
                                     site=self.site,
                                     channel=self.channel3)

        get_container = get_container_by_channel('home2')
        self.assertEqual(len(get_container), 6)

    def test_get_channel_with_magicdate(self):
        date = timezone.now() - timezone.timedelta(days=30)
        for i in self.count_container_create:
            Container.objects.create(title=u'test 3 {0}'.format(i),
                                     user=self.user,
                                     published=True,
                                     site=self.site,
                                     channel=self.channel,
                                     date_available=date
                                     )

        containers = get_container_by_channel('home',
                                              magic_date='30 days ago')

        self.assertEqual(containers.count(), len(self.count_container_create))
