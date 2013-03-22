# -*- coding: utf-8 -*-
from django.utils import timezone
from .models import Channel


def channel_context(request):
    """ Channel context processors
    """
    opps_menu = Channel.objects.filter(date_available__lte=timezone.now(),
                                       published=True)

    return {'opps_menu': opps_menu}
