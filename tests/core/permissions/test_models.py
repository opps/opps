#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from django.test import TestCase, Client
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

from opps.channels.models import Channel
from opps.core.permissions.models import Permission


User = get_user_model()


class PermissionModelTest(TestCase):

    def test_create(self):
        user = User.objects.create(username='user')
        instance = Permission.objects.create(user=user, published=True)
        self.assertTrue(instance)

    def test_empty_get_by_user(self):
        user = User.objects.create(username='another')
        result = Permission.get_by_user(user)

        self.assertEqual(len(result['sites_id']), 0)
        self.assertEqual(len(result['channels_id']), 0)

    def test_get_by_user(self):
        user = User.objects.create(username='john_doe')
        site = Site.objects.all()[0]
        channel = Channel.objects.create(
            name='Home',
            slug='home',
            site=site,
            user=user
        )
        permission = Permission.objects.create(user=user, published=True)
        permission.channel.add(channel)
        permission.save()

        result = Permission.get_by_user(user)

        self.assertEqual(len(result['sites_id']), 1)
        self.assertEqual(len(result['channels_id']), 1)
        self.assertEqual(result['sites_id'][0], site.pk)
        self.assertEqual(result['channels_id'][0], channel.pk)
