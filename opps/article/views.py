#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from opps.article.models import Post


class OppsList(ListView):

    context_object_name = "context"

    @property
    def template_name(self):
        return 'channel/{0}.html'.format(self.kwargs['channel__long_slug'])

    @property
    def queryset(self):
        return Post.objects.filter(
                channel__long_slug=self.kwargs['channel__long_slug']).all()


class OppsDetail(DetailView):

    context_object_name = "context"

    @property
    def template_name(self):
        return 'article/{0}/{1}.html'.format(
                self.kwargs['channel__long_slug'], self.kwargs['slug'])

    @property
    def queryset(self):
        return Post.objects.filter(
                channel__long_slug=self.kwargs['channel__long_slug'],
                slug=self.kwargs['slug']).all()
