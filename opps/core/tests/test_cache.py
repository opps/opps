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

