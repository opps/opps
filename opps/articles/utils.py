# -*- coding: utf-8 -*-
from django.conf import settings

from opps.articles.models import ArticleBox


def set_context_data(self, SUPER, **kwargs):
    context = super(SUPER, self).get_context_data(**kwargs)
    if len(self.article) >= 1:
        article = self.article[0]
        context['articleboxes'] = ArticleBox.objects.filter(
            channel=article.channel)
        if len(self.article) == 1:
            context['articleboxes'] = context['articleboxes'].filter(
                article=article)
        context['opps_channel'] = article.channel
        context['opps_channel_conf'] = settings.OPPS_CHANNEL_CONF.get(
            article.channel.slug, '')
    return context
