#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.list import ListView as DjangoListView
from django.contrib.sites.models import Site, get_current_site
from django.utils import timezone
from django.conf import settings

from opps.views.generic.base import View

from opps.containers.models import Mirror, ContainerBox


class ListView(View, DjangoListView):
    template_name_suffix = ''

    def get_template_list(self, domain_folder="containers"):
        templates = []

        if not self.long_slug:
            templates.append('{0}/none.html'.format(domain_folder))
            return templates

        list_name = 'list'

        if self.template_name_suffix:
            list_name = "{0}{1}".format(list_name, self.template_name_suffix)

        if self.channel:
            # Check layout, change via admin
            if self.channel.layout != u'default':
                list_name = self.channel.layout

            if self.channel.group and self.channel.parent:
                templates.append('{0}/{1}/{2}.html'.format(
                    domain_folder, self.channel.parent.long_slug, list_name))

                if self.request.GET.get('page') and\
                   self.__class__.__name__ not in\
                   settings.OPPS_PAGINATE_NOT_APP:
                    templates.append('{0}/{1}/{2}_paginated.html'.format(
                        domain_folder, self.channel.parent.long_slug,
                        list_name))

            if self.request.GET.get('page') and\
               self.__class__.__name__ not in settings.OPPS_PAGINATE_NOT_APP:
                templates.append('{0}/{1}/{2}_paginated.html'.format(
                    domain_folder, self.channel.long_slug, list_name))

            templates.append('{0}/{1}/{2}.html'.format(
                domain_folder, self.channel.long_slug, list_name))

            for t in self.channel.get_ancestors()[::-1]:
                templates.append('{0}/{1}/{2}.html'.format(
                    domain_folder, t.long_slug, list_name))
                if self.request.GET.get('page') and\
                   self.__class__.__name__ not in\
                   settings.OPPS_PAGINATE_NOT_APP:
                    templates.append('{0}/{1}/{2}_paginated.html'.format(
                        domain_folder, t.long_slug, list_name))

        if self.request.GET.get('page') and\
           self.__class__.__name__ not in settings.OPPS_PAGINATE_NOT_APP:
            templates.append('{0}/{1}_paginated.html'.format(domain_folder,
                                                             list_name))

        templates.append('{0}/{1}.html'.format(domain_folder, list_name))

        return templates

    def get_template_names(self):
        if self.template_name:
            return [self.template_name]

        domain_folder = self.get_template_folder()
        template_list = self.get_template_list(domain_folder)

        if domain_folder != "containers":
            template_list.extend(self.get_template_list())

        return template_list

    def get_queryset(self):
        self.fallback = getattr(settings, 'OPPS_MULTISITE_FALLBACK', False)
        self.site = get_current_site(self.request)
        self.site_master = Site.objects.order_by('id')[0]
        self.long_slug = self.get_long_slug()

        if not self.long_slug:
            return None

        self.set_channel_rules()

        self.articleboxes = ContainerBox.objects.filter(
            channel__long_slug=self.long_slug)

        is_paginated = self.page_kwarg in self.request.GET

        if not is_paginated:
            for box in self.articleboxes:
                self.excluded_ids.update(
                    box.ordered_containers().values_list('pk', flat=True))

        queryset = super(ListView, self).get_queryset()
        filters = {}
        filters['site_domain__in'] = [self.site.domain]
        filters['channel_long_slug__in'] = self.channel_long_slug
        filters['date_available__lte'] = timezone.now()
        filters['published'] = True
        if self.channel and self.channel.is_root_node() and not is_paginated:
            filters['show_on_root_channel'] = True

        # CONTAINER FILTERS
        if self.request.GET.get('type'):
            filters['child_class'] = self.request.GET.get('type')

        if self.fallback and self.site != self.site_master:
            filters.get('site_domain__in', []).append(self.site_master.domain)
        queryset = queryset.filter(**filters)
        if self.excluded_ids:
            queryset = queryset.exclude(
                pk__in=self.excluded_ids)

        # Excluded mirror on root channel
        mirror_excluded = [mirror.id for mirror in Mirror.objects.filter(
            container__channel_long_slug=self.long_slug)]
        queryset = queryset.exclude(pk__in=mirror_excluded)

        return queryset._clone()
