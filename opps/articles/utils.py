# -*- coding: utf-8 -*-
from django.utils import timezone

from opps.articles.models import ArticleBox, Article


def set_context_data(self, SUPER, **kwargs):
    context = super(SUPER, self).get_context_data(**kwargs)

    article = Article.objects.filter(
        site=self.site,
        channel_long_slug__in=self.channel_long_slug,
        date_available__lte=timezone.now(),
        published=True)
    context['posts'] = article.filter(child_class='Post')[:self.limit]
    context['albums'] = article.filter(child_class='Album')[:self.limit]

    context['channel'] = {}
    context['channel']['long_slug'] = self.long_slug
    context['channel']['slug'] = self.channel.slug
    if self.channel:
        context['channel']['level'] = self.channel.get_level()
        context['channel']['root'] = self.channel.get_root()

    context['articleboxes'] = ArticleBox.objects.filter(
        channel__long_slug=self.long_slug)
    if self.slug:
        context['articleboxes'] = context['articleboxes'].filter(
            article__slug=self.slug)

    return context
