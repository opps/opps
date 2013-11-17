#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from django.http import HttpRequest

from opps.core.cache import cache_page


class DecoratorsTest(TestCase):

    def test_cache_page_new_style(self):
        """
        Test that we can call cache_page the new way
        """
        def my_view(request):
            return "response"

        my_view_cached = cache_page(123)(my_view)
        self.assertEqual(my_view_cached(HttpRequest()), "response")
        my_view_cached2 = cache_page(123, key_prefix="test")(my_view)
        self.assertEqual(my_view_cached2(HttpRequest()), "response")

    def test_cache_page_is_mobile(self):
        """
        Test that we can call cache_page in mobile page
        """
        def is_mobile_view(request):
            return request.is_mobile

        def mobile_view(request):
            return 'response'

        mobile_view_cached = cache_page(123)(mobile_view)
        is_mobile_view_cached = cache_page(123)(is_mobile_view)
        request = HttpRequest()
        request.is_mobile = True
        self.assertEqual(mobile_view_cached(request), "response")
        self.assertTrue(is_mobile_view_cached(request))
