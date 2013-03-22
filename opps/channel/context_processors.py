# -*- coding: utf-8 -*-
from .models import Channel


def channel_context(request):
    return {'opps_menu': Channel.objects.all()}
