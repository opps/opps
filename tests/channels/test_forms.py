#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

from opps.channels.models import Channel
from opps.channels.forms import ChannelAdminForm


class ChannelFormTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username=u'test', password='test')
        self.site = Site.objects.filter(name=u'example.com').get()
        self.parent = Channel.objects.create(name=u'Home', slug=u'home',
                                             description=u'home page',
                                             site=self.site, user=self.user)

    def test_init(self):
        """
        Test successful init without data
        """
        form = ChannelAdminForm(instance=self.parent)
        self.assertTrue(isinstance(form.instance, Channel))
        self.assertEqual(form.instance.pk, self.parent.pk)
        self.assertEqual(
            int(form.fields['slug'].widget.attrs['maxlength']), 150)

    def test_default_choices_layout(self):
        """
        Check choices default in layout field
        """
        form = ChannelAdminForm(instance=self.parent)
        self.assertTrue(form.fields['layout'].choices)
        self.assertEqual([c for c in form.fields['layout'].choices],
                         [(u'default', u'Default')])

    def test_readonly_slug(self):
        """
        Check readonly field slug
        """
        form = ChannelAdminForm(instance=self.parent)
        self.assertTrue(form.fields['slug'].widget.attrs['readonly'])

        form_2 = ChannelAdminForm()
        self.assertNotIn('readonly', form_2.fields['slug'].widget.attrs)
