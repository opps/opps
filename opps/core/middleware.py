# -*- coding: utf-8 -*-
import re
import random
from types import MethodType

from django.contrib.sites.models import Site
from django.contrib.sites.models import get_current_site
from django.http import HttpResponseRedirect
from django.conf import settings
from django.http import SimpleCookie, HttpRequest

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
            if not 'channel' in response.context_data:
                site = get_current_site(request)
                response.context_data['channel'] = Channel.objects\
                        .get_homepage(site=site or Site.objects.get(pk=1))
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
        settings.CACHE_MIDDLEWARE_KEY_PREFIX = u"opps_site-{}".format(site.id)


def _is_mobile(request):
    u"""Used django-mobile core

    https://github.com/gregmuellegger/django-mobile/blob/3093a9791e5e812021e49
    3226e5393033115c8bf/django_mobile/middleware.py
    """

    http_accept_regex = re.compile("application/vnd\.wap\.xhtml\+xml",
                                   re.IGNORECASE)

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
    user_agents_test_match = r'^(?:%s)' % '|'.join(user_agents_test_match)

    user_agents_test_match_regex = re.compile(
        user_agents_test_match, re.IGNORECASE)
    user_agents_test_search_regex = re.compile(
        user_agents_test_search, re.IGNORECASE)
    user_agents_exception_search_regex = re.compile(
        user_agents_exception_search, re.IGNORECASE)

    is_mobile = False
    if 'HTTP_ACCEPT' in request.META or 'HTTP_USER_AGENT' in request.META:
        http_accept = request.META.get('HTTP_ACCEPT', '')

        if http_accept_regex.search(http_accept):
            is_mobile = True
        else:
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            if user_agents_test_search_regex.search(user_agent):
                if not user_agents_exception_search_regex.search(user_agent):
                    is_mobile = True

        if not is_mobile:
            if user_agents_test_match_regex.match(user_agent):
                is_mobile = True

        request.is_mobile = is_mobile
    return is_mobile


class MobileDetectionMiddleware(object):

    def process_request(self, request):
        is_mobile = _is_mobile(request)
        settings.TEMPLATE_DIRS = settings.TEMPLATE_DIRS_WEB
        if is_mobile and settings.OPPS_CHECK_MOBILE:

            # set cache prefix randon in mobile device
            settings.CACHE_MIDDLEWARE_KEY_PREFIX = u"opps_site-{}-{}".format(
                settings.SITE_ID, random.getrandbits(32))

            settings.TEMPLATE_DIRS = settings.TEMPLATE_DIRS_MOBILE
            if settings.OPPS_DOMAIN_MOBILE and \
               request.META.get('HTTP_HOST', '') != \
               settings.OPPS_DOMAIN_MOBILE:
                return HttpResponseRedirect(u"{}://{}{}".format(
                    settings.OPPS_PROTOCOL_MOBILE,
                    settings.OPPS_DOMAIN_MOBILE,
                    request.META.get('PATH_INFO', '')))


def _set_cookie(self, key, value='', max_age=None, expires=None, path='/',
                domain=None, secure=False):
    self._resp_cookies[key] = value
    self.COOKIES[key] = value
    if max_age is not None:
        self._resp_cookies[key]['max-age'] = max_age
    if expires is not None:
        self._resp_cookies[key]['expires'] = expires
    if path is not None:
        self._resp_cookies[key]['path'] = path
    if domain is not None:
        self._resp_cookies[key]['domain'] = domain
    if secure:
        self._resp_cookies[key]['secure'] = True


def _delete_cookie(self, key, path='/', domain=None):
    self.set_cookie(key, max_age=0, path=path, domain=domain,
                    expires='Thu, 01-Jan-1970 00:00:00 GMT')
    try:
        del self.COOKIES[key]
    except KeyError:
        pass


class MobileRedirectMiddleware(object):
    """
    Allows setting and deleting of cookies from requests in exactly the same
    way as responses.

    request.set_cookie('name', 'value')

    The set_cookie and delete_cookie are exactly the same as the ones built
    into the Django HttpResponse class.

    http://docs.djangoproject.com/en/dev/ref/request-response
        /#django.http.HttpResponse.set_cookie
    """
    def process_request(self, request):

        domain = request.META.get('HTTP_HOST', '')
        mobile_domain = settings.OPPS_DOMAIN_MOBILE

        current_cookie = request.COOKIES.get('template_mode', None)
        template_mode = request.GET.get('template_mode', None)
        settings.TEMPLATE_DIRS = settings.TEMPLATE_DIRS_WEB

        is_mobile_domain = domain == mobile_domain

        if not template_mode and not current_cookie:
            if is_mobile_domain:
                template_mode = u'mobile'
            else:
                return

        if is_mobile_domain and template_mode == u'desktop':
            prot = settings.OPPS_PROTOCOL_WEB
            web_domain = settings.OPPS_DOMAIN_WEB
            url = u"{}://{}/?template_mode=desktop".format(prot, web_domain)
            return HttpResponseRedirect(url)
        elif not is_mobile_domain and template_mode == u'mobile':
            prot = settings.OPPS_PROTOCOL_MOBILE
            url = u"{}://{}/?template_mode=mobile".format(prot, mobile_domain)

            # set cache prefix randon in mobile device
            settings.CACHE_MIDDLEWARE_KEY_PREFIX = u"opps_site-{}-{}".format(
                settings.SITE_ID, random.getrandbits(32))

            return HttpResponseRedirect(url)

        request._resp_cookies = SimpleCookie()
        request.set_cookie = MethodType(_set_cookie, request, HttpRequest)
        request.delete_cookie = MethodType(
            _delete_cookie, request, HttpRequest
        )

        if template_mode:
            request.set_cookie('template_mode', template_mode)
            current_cookie = template_mode

        if current_cookie and current_cookie.strip().lower() == u"mobile":
            settings.TEMPLATE_DIRS = settings.TEMPLATE_DIRS_MOBILE

    def process_response(self, request, response):
        if hasattr(request, '_resp_cookies') and request._resp_cookies:
            response.cookies.update(request._resp_cookies)

        return response
