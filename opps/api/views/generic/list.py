#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sites.models import get_current_site
from django.utils import timezone

from rest_framework.generics import ListAPIView as RestListAPIView
from rest_framework.generics import ListCreateAPIView

from opps.views.generic.base import View
from opps.containers.models import ContainerBox


class ListView(View, RestListAPIView):
    def get_queryset(self):
        self.long_slug = self.get_long_slug()
        self.site = get_current_site(self.request)

        if not self.long_slug:
            return None

        self.set_channel_rules()

        self.articleboxes = ContainerBox.objects.filter(
            channel__long_slug=self.long_slug)

        for box in self.articleboxes:
            self.excluded_ids.update([a.pk for a in box.ordered_containers()])

        queryset = super(ListView, self).get_queryset()
        filters = {}
        filters['site_domain'] = self.site.domain
        try:
            if queryset.model._meta.get_field_by_name('channel_long_slug'):
                filters['channel_long_slug__in'] = self.channel_long_slug
        except:
            pass
        filters['date_available__lte'] = timezone.now()
        filters['published'] = True
        queryset = queryset.filter(**filters).exclude(pk__in=self.excluded_ids)

        return queryset._clone()


class ListCreateView(ListCreateAPIView, ListView):
    pass
