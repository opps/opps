#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sites.models import get_current_site
from django.utils import timezone
from django.conf import settings

from opps.views.generic.list import ListView
from opps.containers.views import ContainerList
from opps.articles.models import Album


class AlbumList(ContainerList):
    model = Album
    type = 'album'


class AlbumChannelList(ListView):

    def get_template_names(self):
        templates = []

        domain_folder = self.get_template_folder()
        list_name = 'list'

        templates.append('{}/{}/{}.html'.format(
            self.model._meta.app_label,
            self.model._meta.module_name, list_name))

        if self.request.GET.get('page') and\
           self.__class__.__name__ not in\
           settings.OPPS_PAGINATE_NOT_APP:
            templates.append('{}/{}/{}/{}_paginated.html'.format(
                domain_folder, self.model._meta.app_label,
                self.model._meta.module_name, list_name))

        return templates

    def get_queryset(self):
        self.site = get_current_site(self.request)

        queryset = super(AlbumChannelList, self).get_queryset()
        filters = {}
        filters['site_domain'] = self.site.domain
        filters['date_available__lte'] = timezone.now()
        filters['published'] = True
        filters['show_on_root_channel'] = True
        queryset = queryset.filter(**filters)

        return queryset._clone()
