# coding: utf-8
from datetime import date

from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

from opps.channels.models import Channel
from opps.containers.models import Container


class SitemapTest(TestCase):

    def setUp(self):
        self.domain = 'example.com' if Site._meta.installed else 'testserver'
        self.urls = 'opps.contrib.sitemaps.urls'
        self.base_url = 'http://{0}'.format(self.domain)
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

    def test_sitemap_index(self):
        response = self.client.get('/sitemap.xml')
        expected_content = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<sitemap><loc>{0}/sitemap-containers.xml</loc></sitemap></sitemapindex>
""".format(self.base_url).replace('\n', '')
        self.assertXMLEqual(response.content.decode('utf-8'), expected_content)

    def test_sitemap_container(self):
        response = self.client.get('/sitemap-containers.xml')
        expected_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>{0}</loc><lastmod>{1}</lastmod><priority>0.6</priority></url>
</urlset>""".format(self.container.get_http_absolute_url(),
                    self.container.date_available.date()).replace('\n', '')
        self.assertXMLEqual(response.content.decode('utf-8'), expected_content)
