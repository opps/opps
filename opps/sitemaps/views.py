# coding: utf-8
from functools import wraps
from calendar import timegm

from django.contrib.sites.models import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.http import http_date
from django.conf import settings
from django.views.decorators.cache import cache_page


def x_robots_tag(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        response['X-Robots-Tag'] = 'noindex, noodp, noarchive'
        return response
    return inner


@x_robots_tag
@cache_page(86400)
def sitemap(request, sitemaps, section=None,
            template_name='sitemap.xml', content_type='application/xml'):

    req_protocol = 'https' if request.is_secure() else 'http'
    req_site = get_current_site(request)

    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps = [sitemaps[section]]
    else:
        maps = list(six.itervalues(sitemaps))
    page = request.GET.get("p", 1)

    urls = []
    context = {}
    for site in maps:
        try:
            if callable(site):
                site = site()
            urls.extend(site.get_urls(page=page, site=req_site,
                                      protocol=req_protocol))
        except EmptyPage:
            raise Http404("Page %s empty" % page)
        except PageNotAnInteger:
            raise Http404("No page '%s'" % page)

    sitemap_language = getattr(settings, 'SITEMAP_LANGUAGE', 'en')
    publication_name = getattr(settings, 'SITEMAP_PUBLICATION_NAME', 'Opps')

    context = {
        'urlset': urls,
        'sitemap_language': sitemap_language,
        'publication_name': publication_name,
    }

    response = TemplateResponse(request, template_name, context,
                                content_type=content_type)
    if hasattr(site, 'latest_lastmod'):
        # if latest_lastmod is defined for site, set header so as
        # ConditionalGetMiddleware is able to send 304 NOT MODIFIED
        response['Last-Modified'] = http_date(
            timegm(site.latest_lastmod.utctimetuple()))
    return response
