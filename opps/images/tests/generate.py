#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from django.template import Template, Context


class TestImagesTags(TestCase):
    url = 'oppsproject.org/path/image.jpg'
    generate_url_path = 'opps.images.templatetags.images_tags.image_url'

    def render(self, arguments):
        source = u'{% load images_tags %}{% image_url '+ arguments +' %}'
        template = Template(source)
        rendered = template.render(Context({'url': self.url}))
        return rendered.strip()

    def test_templatetag_return(self):
        self.assertTrue(self.render(u'url unsafe=True'))

    def test_should_pass_the_image_url_arg_to_the_helper(self):
        self.assertEqual(self.render(u'url unsafe=True'),
                         u'http://localhost:8888/unsafe/localhost:8000/media/'
                         u'oppsproject.org/path/image.jpg')

    def test_should_pass_kwargs_to_the_helper(self):
        self.assertEqual(self.render(u'url width=300 height=200 unsafe=True'),
                         u'http://localhost:8888/unsafe/300x200/'
                         u'localhost:8000/media/oppsproject.org/path/'
                         u'image.jpg')
