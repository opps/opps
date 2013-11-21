from calendar import timegm
from functools import wraps

from django.contrib.sites.models import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.http import http_date
from django.conf import settings


def x_robots_tag(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        response['X-Robots-Tag'] = 'noindex, noodp, noarchive'
        return response
    return inner


@x_robots_tag
def sitemap(request, sitemaps, section=None,
            template_name='sitemap.xml', content_type='application/xml'):

    req_protocol = getattr(request, 'scheme', 'http')
    req_site = get_current_site(request)

    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps = [sitemaps[section]]
    else:
        maps = list(six.itervalues(sitemaps))
    page = request.GET.get("p", 1)

    urls = []
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
    context = {
        'urlset': urls,
        'publication_name': getattr(settings, 'OPPS_SITEMAP_PUBLICATION_NAME',
                                    u'Opps CMS'),
        'sitemap_language': getattr(settings, 'OPPS_SITEMAP_LANGUAGE',
                                    u'en')
    }
    response = TemplateResponse(request, template_name, context,
                                content_type=content_type)
    if hasattr(site, 'latest_lastmod'):
        # if latest_lastmod is defined for site, set header so as
        # ConditionalGetMiddleware is able to send 304 NOT MODIFIED
        response['Last-Modified'] = http_date(
            timegm(site.latest_lastmod.utctimetuple()))
    return response
