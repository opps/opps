#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.list import ListView as DjangoListView
from django.contrib.sites.models import get_current_site
from django.utils import timezone
from django.conf import settings

from opps.views.generic.base import View

from opps.containers.models import ContainerBox


class ListView(View, DjangoListView):

    def get_template_names(self):
        templates = []

        domain_folder = self.get_template_folder()

        if self.channel:
            if self.channel.group and self.channel.parent:
                templates.append('{}/{}/list.html'.format(
                    domain_folder, self.channel.parent.long_slug))

                if self.request.GET.get('page') and\
                   self.__class__.__name__ not in\
                   settings.OPPS_PAGINATE_NOT_APP:
                    templates.append('{}/{}/list_paginate.html'.format(
                        domain_folder, self.channel.parent.long_slug))

            if self.request.GET.get('page') and\
               self.__class__.__name__ not in settings.OPPS_PAGINATE_NOT_APP:
                templates.append('{}/{}/list_paginate.html'.format(
                    domain_folder, self.channel.long_slug))

            templates.append('{}/{}/list.html'.format(
                domain_folder, self.channel.long_slug))

        templates.append('{}/list.html'.format(domain_folder))

        return templates

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
        filters['channel_long_slug__in'] = self.channel_long_slug
        filters['date_available__lte'] = timezone.now()
        filters['published'] = True
        filters['show_on_root_channel'] = True
        queryset = queryset.filter(**filters).exclude(pk__in=self.excluded_ids)

        return queryset._clone()
