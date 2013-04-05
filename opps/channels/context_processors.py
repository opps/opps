# -*- coding: utf-8 -*-
from django.utils import timezone
from django.conf import settings
from django.contrib.sites.models import get_current_site

from .models import Channel


def channel_context(request):
    """ Channel context processors
    """
    site = get_current_site(request)
    opps_menu = Channel.objects.filter(site=site,
                                       date_available__lte=timezone.now(),
                                       published=True,
                                       show_in_menu=True).order_by('order')

    return {'opps_menu': opps_menu,
            'opps_channel_conf_all': settings.OPPS_CHANNEL_CONF}
