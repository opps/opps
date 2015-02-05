#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from opps.channels.models import Channel
from opps.core.permissions.models import Permission, PermissionGroup


User = get_user_model()


class PermissionModelTest(TestCase):

    def test_create(self):
        user = User.objects.create(username='user')
        instance = Permission.objects.create(user=user)
        self.assertTrue(instance)

    def test_empty_get_by_user(self):
        user = User.objects.create(username='another')
        result = Permission.get_by_user(user)

        self.assertEqual(len(result['sites_id']), 0)
        self.assertEqual(len(result['all_sites_id']), 0)
        self.assertEqual(len(result['channels_id']), 0)
        self.assertEqual(len(result['channels_sites_id']), 0)

    def test_get_by_user_with_user_permission(self):
        user = User.objects.create(username='john_doe')
        site = Site.objects.all()[0]
        channel = Channel.objects.create(
            name='Home',
            slug='home',
            site=site,
            user=user
        )
        permission = Permission.objects.create(user=user)
        permission.channel.add(channel)
        permission.save()

        result = Permission.get_by_user(user)

        self.assertTrue(site.pk in result['all_sites_id'])
        self.assertTrue(channel.pk in result['channels_id'])

    def test_get_by_user_with_group_permission(self):
        group = Group.objects.create(name='programmers')
        user = User.objects.create(username='john_doe')
        user.groups.add(group)

        site = Site.objects.all()[0]
        channel = Channel.objects.create(
            name='Home',
            slug='home',
            site=site,
            user=user
        )
        permission = PermissionGroup.objects.create(group=group)
        permission.channel.add(channel)
        permission.save()

        result = Permission.get_by_user(user)

        self.assertTrue(site.pk in result['all_sites_id'])
        self.assertTrue(channel.pk in result['channels_id'])
