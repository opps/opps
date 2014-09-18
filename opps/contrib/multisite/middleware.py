#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.conf import settings


class DynamicSiteMiddleware(object):

    def hosting_parse(self, hosting):
        """
        Returns ``(host, port)`` for ``hosting`` of the form ``'host:port'``.

        If hosting does not have a port number, ``port`` will be None.
        """
        if ':' in hosting:
            return hosting.rsplit(':', 1)
        return hosting, None

    def get_hosting(self, hosting):
        domain, port = self.hosting_parse(hosting)
        if domain in settings.OPPS_DEFAULT_URLS:
            domain = 'example.com'
        try:
            return Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            return Site.objects.order_by('id')[0]

    def process_request(self, request):
        hosting = request.get_host().lower()
        site = self.get_hosting(hosting)

        request.site = site
        settings.SITE_ID = site.id
        settings.CACHE_MIDDLEWARE_KEY_PREFIX = "opps_site-{0}".format(site.id)
