#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from opps.containers.models import Container
from opps.channels.models import Channel
from opps.db import Db

from .models import Notification


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
        self.notification = Notification.objects.create(
            user=self.user,
            container=self.container,
            message='Test new notification',
            type='text'
        )

    def test_exist_notification(self):
        noti = Notification.objects.all()[0]
        self.assertTrue(self.notification)
        self.assertTrue(noti)
        self.assertEqual(noti, self.notification)
        self.assertEqual(noti.type, 'text')
        self.assertEqual(noti.id, self.notification.id)

    def test_pubsub_notification(self):
        noti = Notification.objects.all()[0]
        _db = Db(noti.container.get_absolute_url(),
                 noti.container.id)
        pubsub = _db.object().pubsub()
        pubsub.subscribe(_db.key)

        self.assertTrue(pubsub)
        self.assertEqual(pubsub.channels,
                         set([u'opps_/home/test.html_1']))
