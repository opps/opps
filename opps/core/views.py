#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from opps.core.models.article import Post


class OppsDetail(DetailView):

    context_object_name = "context"
    queryset = Post.objects.all()
