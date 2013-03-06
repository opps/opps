#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView

from opps.article.models import Post


class OppsDetail(DetailView):

    context_object_name = "context"

    @property
    def queryset(self):
        return Post.objects.filter(
                channel__long_slug=self.kwargs['channel__long_slug'],
                slug=self.kwargs['slug']).all()
