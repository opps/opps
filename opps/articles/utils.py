# -*- coding: utf-8 -*-
from opps.articles.models import ArticleBox


def set_context_data(self, SUPER, **kwargs):
    context = super(SUPER, self).get_context_data(**kwargs)

    context['articleboxes'] = ArticleBox.objects.filter(
        channel__long_slug=self.long_slug)
    if self.slug:
        context['articleboxes'] = context['articleboxes'].filter(
            article__slug=self.slug)

    return context
