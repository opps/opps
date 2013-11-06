#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sites.models import get_current_site
from django.utils import timezone

from rest_framework.generics import ListAPIView as RestListAPIView
from rest_framework.generics import UpdateAPIView as RestUpdateAPIView
from rest_framework.generics import (
    RetrieveUpdateAPIView as RestRetrieveUpdateAPIView)

from .base import BaseView


class DetailView(BaseView, RestListAPIView):
    def get_queryset(self):
        self.site = get_current_site(self.request)
        self.slug = self.kwargs.get('slug')
        self.long_slug = self.get_long_slug()
        if not self.long_slug:
            return None

        self.set_channel_rules()

        filters = {}
        filters['site_domain'] = self.site.domain
        filters['channel_long_slug'] = self.long_slug
        filters['slug'] = self.slug

        preview_enabled = self.request.user and self.request.user.is_staff

        if not preview_enabled:
            filters['date_available__lte'] = timezone.now()
            filters['published'] = True

        queryset = super(DetailView, self).get_queryset()
        return queryset.filter(**filters)._clone()


class UpdateAPIView(RestUpdateAPIView, DetailView):
    pass


class RetrieveUpdateAPIView(RestRetrieveUpdateAPIView, DetailView):
    pass
