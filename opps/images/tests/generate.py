#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from django.template import Template, Context
from django.conf import settings


class TestImagesTagsImageUrl(TestCase):
    url = 'oppsproject.org/path/image.jpg'
    generate_url_path = 'opps.images.templatetags.images_tags.image_url'

    def render(self, arguments):
        source = u'{% load images_tags %}{% image_url ' + arguments + ' %}'
        template = Template(source)
        rendered = template.render(Context({'url': self.url}))
        return rendered.strip()

    def test_templatetag_return(self):
        self.assertTrue(self.render(u'url unsafe=True'))

    def test_should_pass_the_image_url_arg_to_the_helper(self):
        if settings.THUMBOR_ENABLED:
            image_url = (u'http://localhost:8888/unsafe/localhost:8000/media/'
                         u'oppsproject.org/path/image.jpg')
        else:
            image_url = self.url

        self.assertEqual(self.render(u'url unsafe=True'), image_url)

    def test_should_pass_kwargs_to_the_helper(self):
        if settings.THUMBOR_ENABLED:
            image_url = (u'http://localhost:8888/unsafe/300x200/'
                         u'localhost:8000/media/oppsproject.org/path/'
                         u'image.jpg')
        else:
            image_url = self.url

        self.assertEqual(self.render(u'url width=300 height=200 unsafe=True'),
                         image_url)
