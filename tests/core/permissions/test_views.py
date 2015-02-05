#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

from opps.channels.models import Channel
from opps.core.permissions.models import Permission


def get_url(app_label, model_name):
    return "{}?term=&app_label={}&model_name={}".format(
        reverse('permissions:grp_autocomplete_lookup'),
        app_label,
        model_name
    )


class OppsAutocompleteLookupTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username='test', is_staff=True)
        self.user.set_password('test')
        self.user.save()

        self.user2 = User.objects.create(username='test2', is_staff=True)
        self.user2.set_password('test')
        self.user2.save()

        self.site = Site.objects.all()[0]
        self.channel_allowed = Channel.objects.create(
            name='Home',
            slug='home',
            site=self.site,
            user=self.user
        )
        self.channel_not_allowed = Channel.objects.create(
            name='Top secret',
            slug='top-secret',
            site=self.site,
            user=self.user
        )
        self.permission = Permission.objects.create(user=self.user)
        self.permission.channel.add(self.channel_allowed)
        self.permission.save()

        self.client = Client()

    def test_user_has_permission(self):
        self.client.login(username='test', password='test')
        response = self.client.get(get_url('channels', 'Channel'))
        result = json.loads(response.content)
        pk = self.channel_allowed.pk

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(filter(lambda x: x['value'] == pk, result)), 1)

    def test_user_hasnt_permission(self):
        self.client.login(username='test', password='test')
        response = self.client.get(get_url('channels', 'Channel'))
        result = json.loads(response.content)
        pk = self.channel_not_allowed.pk

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(filter(lambda x: x['value'] == pk, result)), 0)

    def test_user_without_permission(self):
        self.client.login(username='test2', password='test')
        response = self.client.get(get_url('channels', 'Channel'))
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['value'], None)
        self.assertEqual(result[0]['label'], '0 results')
