# -*- coding: utf-8 -*-
from django.utils import timezone
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.core.cache import cache

from .models import Channel


def channel_context(request):
    """ Channel context processors
    """
    site = get_current_site(request)
    if settings.OPPS_MENU:
        opps_menu = cache.get('opps_menu')
        if not opps_menu:
            opps_menu = [channel for channel in Channel.objects.filter(
                site=site,
                date_available__lte=timezone.now(),
                published=True,
                show_in_menu=True).distinct().order_by('order')]
            cache.set('opps_menu', opps_menu, settings.OPPS_CACHE_EXPIRE)
    else:
        opps_menu = []

    return {'opps_menu': opps_menu,
            'opps_channel_conf_all': settings.OPPS_CHANNEL_CONF,
            'site': site}
