#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from opps.containers.models import ContainerBox
from opps.channels.models import Channel


class ContainerBoxTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()

        self.channel = Channel.objects.create(name=u'Home', slug=u'home',
                                              description=u'home page',
                                              site=self.site, user=self.user)

    def test_create_containerbox(self):
        self.count_container_create = [1, 2, 3, 4, 5]

        for i in self.count_container_create:
            ContainerBox.objects.create(title=u'test {0}'.format(i),
                                        user=self.user,
                                        published=True,
                                        site=self.site,
                                        channel=self.channel)

        ContainerBox.objects.create(title=u'test channel 2',
                                    user=self.user,
                                    published=True,
                                    site=self.site,
                                    channel=self.channel)

    def test_create_and_delete_containersbox(self):
        containerbox = ContainerBox.objects.create(title=u'Test 01',
                                                   slug=u'test-01',
                                                   user=self.user,
                                                   published=True,
                                                   site=self.site,
                                                   channel=self.channel,
                                                   channel_long_slug=self.channel.long_slug)

        containerbox.delete()

    def test_edit_containersbox(self):
        containerbox = ContainerBox.objects.create(title=u'Test 02',
                                                   slug=u'test-02',
                                                   user=self.user,
                                                   published=True,
                                                   site=self.site,
                                                   channel=self.channel,
                                                   channel_long_slug=self.channel.long_slug)

        containerbox.title = u'Changed title'
        containerbox.save()
