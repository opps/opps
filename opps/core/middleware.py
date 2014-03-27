# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.contrib.sites.models import get_current_site
from django.conf import settings

from opps.channels.models import Channel


class URLMiddleware(object):
    def process_request(self, request):
        """
        if the requested site is id 2 it
        will force the ROOT_URLCONF = 'yourproject.urls_2.py'
        """
        self.request = request
        site = get_current_site(request)
        if site.id > 1:
            prefix = "_{0}".format(site.id)
            self.request.urlconf = settings.ROOT_URLCONF + prefix


class TemplateContextMiddleware(object):
    """
    Include aditional items in response context_data
    """
    def process_template_response(self, request, response):
        if hasattr(response, 'context_data'):
            if 'channel' not in response.context_data:
                site = get_current_site(request)
                response.context_data['channel'] = Channel.objects\
                        .get_homepage(site=site or Site.objects.get(pk=1))
        return response
