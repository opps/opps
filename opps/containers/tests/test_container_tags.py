#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from opps.containers.models import Container
from opps.channels.models import Channel

from ..templatetags.container_tags import get_containers_by


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
