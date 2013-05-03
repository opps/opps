# -*- coding: utf-8 -*-
import re
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
        try:
            if not 'channel' in response.context_data:
                site = get_current_site(request)
                response.context_data['channel'] = Channel.objects\
                        .get_homepage(site=site or Site.objects.get(pk=1))
        except AttributeError:
            pass
        return response


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
            return Site.objects.all()[0]

    def process_request(self, request):
        hosting = request.get_host().lower()
        site = self.get_hosting(hosting)

        settings.SITE_ID = site.id


class MobileDetectionMiddleware(object):
    u"""Used django-mobile core

    https://github.com/gregmuellegger/django-mobile/blob/3093a9791e5e812021e49
    3226e5393033115c8bf/django_mobile/middleware.py
    """

    user_agents_test_match = (
        "w3c ", "acs-", "alav", "alca", "amoi", "audi",
        "avan", "benq", "bird", "blac", "blaz", "brew",
        "cell", "cldc", "cmd-", "dang", "doco", "eric",
        "hipt", "inno", "ipaq", "java", "jigs", "kddi",
        "keji", "leno", "lg-c", "lg-d", "lg-g", "lge-",
        "maui", "maxo", "midp", "mits", "mmef", "mobi",
        "mot-", "moto", "mwbp", "nec-", "newt", "noki",
        "xda", "palm", "pana", "pant", "phil", "play",
        "port", "prox", "qwap", "sage", "sams", "sany",
        "sch-", "sec-", "send", "seri", "sgh-", "shar",
        "sie-", "siem", "smal", "smar", "sony", "sph-",
        "symb", "t-mo", "teli", "tim-", "tosh", "tsm-",
        "upg1", "upsi", "vk-v", "voda", "wap-", "wapa",
        "wapi", "wapp", "wapr", "webc", "winw", "winw",
        "xda-",)

    user_agents_test_search = u"(?:%s)" % u'|'.join((
        'up.browser', 'up.link', 'mmp', 'symbian', 'smartphone', 'midp',
        'wap', 'phone', 'windows ce', 'pda', 'mobile', 'mini', 'palm',
        'netfront', 'opera mobi',))

    user_agents_exception_search = u"(?:%s)" % u'|'.join(('ipad',))

    http_accept_regex = re.compile("application/vnd\.wap\.xhtml\+xml",
                                   re.IGNORECASE)

    def __init__(self):
        user_agents_test_match = r'^(?:%s)' % '|'.join(
            self.user_agents_test_match)
        self.user_agents_test_match_regex = re.compile(
            user_agents_test_match, re.IGNORECASE)
        self.user_agents_test_search_regex = re.compile(
            self.user_agents_test_search, re.IGNORECASE)
        self.user_agents_exception_search_regex = re.compile(
            self.user_agents_exception_search, re.IGNORECASE)

    def process_request(self, request):
        is_mobile = False

        if 'HTTP_USER_AGENT' in request.META:
            user_agent = request.META['HTTP_USER_AGENT']

            if self.user_agents_test_search_regex.search(user_agent) and \
               not self.user_agents_exception_search_regex.search(user_agent):
                is_mobile = True
            else:
                if 'HTTP_ACCEPT' in request.META:
                    http_accept = request.META['HTTP_ACCEPT']
                    if self.http_accept_regex.search(http_accept):
                        is_mobile = True

            if not is_mobile:
                if self.user_agents_test_match_regex.match(user_agent):
                    is_mobile = True

        settings.TEMPLATE_DIRS = settings.TEMPLATE_DIRS_WEB
        if is_mobile and settings.OPPS_CHECK_MOBILE:
            settings.TEMPLATE_DIRS = settings.TEMPLATE_DIRS_MOBILE
