# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
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

        return get_object_or_404(Site, domain=domain)

    def process_request(self, request):
        hosting = request.get_host().lower()
        site = self.get_hosting(hosting)

        settings.SITE_ID = site.id
