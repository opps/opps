# -*- coding: utf-8 -*-
from django.conf import settings


def set_context_data(self, SUPER, **kwargs):
    context = super(SUPER, self).get_context_data(**kwargs)
    if len(self.article) >= 1:
        article = self.article[0]
        context['opps_channel'] = article.channel
        context['opps_channel_conf'] = settings.OPPS_CHANNEL_CONF\
                .get(article.channel.slug, '')
    return context
