#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from opps.channels.models import Channel
from opps.boxes.models import QuerySet, BaseBox


class BoxesFields(TestCase):

    def test_name(self):
        field = QuerySet._meta.get_field_by_name(u"name")[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)

    def test_slug(self):
        field = QuerySet._meta.get_field_by_name(u"slug")[0]
        self.assertEqual(field.__class__, models.SlugField)
        self.assertTrue(field.db_index)
        self.assertEqual(field.max_length, 150)
        self.assertTrue(field.unique)

    def test_model(self):
        field = QuerySet._meta.get_field_by_name(u"model")[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 150)

    def test_limit(self):
        field = QuerySet._meta.get_field_by_name(u"limit")[0]
        self.assertEqual(field.__class__, models.PositiveIntegerField)
        self.assertEqual(field.default, 7)

    def test_offset(self):
        field = QuerySet._meta.get_field_by_name(u"offset")[0]
        self.assertEqual(field.__class__, models.PositiveIntegerField)
        self.assertEqual(field.default, 0)

    def test_order(self):
        field = QuerySet._meta.get_field_by_name(u"order")[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 1)
        self.assertEqual(field.choices, (('-', 'DESC'), ('+', 'ASC')))

    def test_channel(self):
        field = QuerySet._meta.get_field_by_name(u"filters")[0]
        self.assertEqual(field.__class__, models.TextField)
        self.assertEqual(
            field.help_text,
            u"Json format extra filters for queryset"
        )
        self.assertTrue(field.blank)
        self.assertTrue(field.null)


class BaseBoxFields(TestCase):

    def test_name(self):
        field = BaseBox._meta.get_field_by_name(u"name")[0]
        self.assertEqual(field.__class__, models.CharField)
        self.assertEqual(field.max_length, 140)

    def test_slug(self):
        field = BaseBox._meta.get_field_by_name(u"slug")[0]
        self.assertEqual(field.__class__, models.SlugField)
        self.assertTrue(field.db_index)
        self.assertEqual(field.max_length, 150)


class QuerySetTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.channel = Channel.objects.create(name=u'Home', slug=u'home',
                                              description=u'home page',
                                              site=self.site, user=self.user)
        self.model = u"containers.Container"

        self.filters = json.dumps({"employees": [{"firstName": "Anna",
                                                 "lastName": "Smith"}, ]})

        self.queryset = QuerySet.objects.create(name=u"Query",
                                                slug=u"query",
                                                user=self.user,
                                                model=self.model,
                                                channel=self.channel,
                                                filters=self.filters)

    def test_queryset_fields(self):
        self.assertEqual(self.queryset.name, u"Query")
        self.assertEqual(self.queryset.slug, u"query")
        self.assertEqual(self.queryset.user, self.user)
        self.assertEqual(self.queryset.model, self.model)
        self.assertEqual(self.queryset.channel, self.channel)
        self.assertEqual(self.queryset.filters, self.filters)

    def test_have_filters_in_clean_function(self):
        self.assertTrue(self.filters)
        self.assertEqual(json.loads(self.filters), {u'employees': [{
            u'lastName': u'Smith',
            u'firstName': u'Anna'}]})

    def test_not_filters_in_clean_function(self):
        invalid = QuerySet.objects.create(name=u"Query Test",
                                          slug=u"query_test",
                                          user=self.user,
                                          model=self.model,
                                          channel=self.channel,
                                          filters=None)

        self.assertEqual(None, invalid.filters)
        self.assertFalse(invalid.filters)
