# -*- coding: utf-8 -*-
import re
import random

from types import MethodType

from django.http import HttpResponseRedirect
from django.http import SimpleCookie
from django.http import HttpRequest
from django.conf import settings


try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

# Instead changing ``settings.TEMPLATE_DIRS`` on the fly, what could
# not work properly when there is concurrent requests, we use
# thread-local variables to determine the template directory used for
# mobile requests, so the template loader
# ``opps.contrib.mobile.template.Loader`` can be used instead to
# define the right templates in each of your project views.
THREAD_LOCALS = local()


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


IGNORE_AGENTS = getattr(settings, 'OPPS_MOBILE_IGNORE_USER_AGENTS', [])

USER_AGENTS_TEST_MATCH = (
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

USER_AGENTS_TEST_SEARCH = u"(?:%s)" % u'|'.join((
    'up.browser', 'up.link', 'mmp', 'symbian', 'smartphone', 'midp',
    'wap', 'phone', 'windows ce', 'pda', 'mobile', 'mini', 'palm',
    'netfront', 'opera mobi',))

USER_AGENTS_EXCEPTION_SEARCH = u"(?:%s)" % u'|'.join(('ipad',))

HTTP_ACCEPT_REGEX = re.compile("application/vnd\.wap\.xhtml\+xml",
                               re.IGNORECASE)


def is_mobile_agent(request):
    user_agents_test_match = r'^(?:%s)' % '|'.join(
        USER_AGENTS_TEST_MATCH)
    user_agents_test_match_regex = re.compile(
        user_agents_test_match, re.IGNORECASE)
    user_agents_test_search_regex = re.compile(
        USER_AGENTS_TEST_SEARCH, re.IGNORECASE)
    user_agents_exception_search_regex = re.compile(
        USER_AGENTS_EXCEPTION_SEARCH, re.IGNORECASE)

    is_mobile = False

    if 'HTTP_USER_AGENT' in request.META:
        user_agent = request.META['HTTP_USER_AGENT']

        if user_agents_test_search_regex.search(user_agent) and \
           not user_agents_exception_search_regex.search(user_agent):
            is_mobile = True
        else:
            if 'HTTP_ACCEPT' in request.META:
                http_accept = request.META['HTTP_ACCEPT']
                if HTTP_ACCEPT_REGEX.search(http_accept):
                    is_mobile = True

        if not is_mobile:
            if user_agents_test_match_regex.match(user_agent):
                is_mobile = True

        # Check for ignore user agents
        if IGNORE_AGENTS and user_agent in IGNORE_AGENTS:
            is_mobile = False

    return is_mobile


class MobileDetectionMiddleware(object):
    u"""Used django-mobile core

    https://github.com/gregmuellegger/django-mobile/blob/3093a9791e5e812021e49
    3226e5393033115c8bf/django_mobile/middleware.py
    """

    def process_request(self, request):
        is_mobile = is_mobile_agent(request)
        request.is_mobile = is_mobile
        THREAD_LOCALS.template_dirs = settings.TEMPLATE_DIRS_WEB

        if is_mobile and settings.OPPS_CHECK_MOBILE:
            THREAD_LOCALS.template_dirs = settings.TEMPLATE_DIRS_MOBILE
            if settings.OPPS_DOMAIN_MOBILE and \
               request.META.get('HTTP_HOST', '') != \
               settings.OPPS_DOMAIN_MOBILE:
                return HttpResponseRedirect(u"{0}://{1}{2}".format(
                    settings.OPPS_PROTOCOL_MOBILE,
                    settings.OPPS_DOMAIN_MOBILE,
                    request.path
                ))


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
        THREAD_LOCALS.template_dirs = settings.TEMPLATE_DIRS_WEB

        if hasattr(request, "is_mobile"):
            agent_is_mobile = request.is_mobile
        else:
            agent_is_mobile = is_mobile_agent(request)

        domain_is_mobile = domain == mobile_domain

        request_is_mobile = agent_is_mobile and domain_is_mobile

        if not template_mode and not current_cookie:
            if domain_is_mobile:
                template_mode = u'mobile'
            else:
                return

        if request_is_mobile and template_mode == u'desktop':
            prot = settings.OPPS_PROTOCOL_WEB
            web_domain = settings.OPPS_DOMAIN_WEB
            url = u"{0}://{1}/?template_mode=desktop".format(prot, web_domain)
            return HttpResponseRedirect(url)
        elif not request_is_mobile and template_mode == u'mobile':
            prot = settings.OPPS_PROTOCOL_MOBILE
            url = u"{0}://{1}/?template_mode=mobile".format(prot,
                                                            mobile_domain)

            # set cache prefix randon in mobile device
            settings.CACHE_MIDDLEWARE_KEY_PREFIX = u"opps_site-{0}-{1}".format(
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
            THREAD_LOCALS.template_dirs = settings.TEMPLATE_DIRS_MOBILE

    def process_response(self, request, response):
        if hasattr(request, '_resp_cookies') and request._resp_cookies:
            response.cookies.update(request._resp_cookies)

        return response
