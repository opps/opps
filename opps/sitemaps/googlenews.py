#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sites.models import Site


class GoogleNewsSitemap(GenericSitemap):
    # That's Google News limit. Do not increase it!
    limit = 1000
    sitemap_template = 'sitemap_googlenews.xml'

    def get_urls(self, page=1, site=None):
        if site is None:
            site = Site.objects.get_current()
        sup = super(GoogleNewsSitemap, self)
        old_urls = sup.get_urls(page, site)
        urls = []
        for item in self.paginator.page(page).object_list:
            for url in old_urls:
                loc = "http://%s%s" % (site.domain, self.location(item))
                if url.get('location') == loc:
                    old_urls.remove(url)
                    url['item'] = item
                    urls.append(url)
        return urls
