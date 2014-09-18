#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sites.models import get_current_site
from django.utils import timezone
from django.conf import settings

from opps.views.generic.list import ListView
from opps.containers.views import ContainerList
from opps.containers.models import Container, ContainerBox
from opps.articles.models import Album


class AlbumList(ContainerList):
    model = Album
    type = 'articles'

    def get_template_names(self):
        templates = []

        domain_folder = self.get_template_folder()
        list_name = 'list'

        templates.append('{0}/{1}/{2}.html'.format(
            self.model._meta.app_label,
            self.model._meta.module_name, list_name))

        if self.request.GET.get('page') and\
           self.__class__.__name__ not in\
           settings.OPPS_PAGINATE_NOT_APP:
            templates.append('{0}/{1}/{2}/{3}_paginated.html'.format(
                domain_folder, self.model._meta.app_label,
                self.model._meta.module_name, list_name))

        return templates

    def get_queryset(self):
        # TODO: refatoring, used super()
        self.site = get_current_site(self.request)
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
                    [a.pk for a in box.ordered_containers()])

        filters = {}
        filters['site_domain'] = self.site.domain
        filters['date_available__lte'] = timezone.now()
        filters['published'] = True
        filters['child_class'] = 'Album'
        if self.channel and self.channel.is_root_node() and not is_paginated:
            filters['show_on_root_channel'] = True
        queryset = Container.objects.filter(
            **filters).exclude(pk__in=self.excluded_ids)

        return queryset._clone()


class AlbumChannelList(ListView):
    model = Album
    type = 'articles'
    template_name_suffix = 'album'

    def get_template_list(self, domain_folder="containers"):
        templates = []
        list_name = 'list'

        if self.template_name_suffix:
            list_fullname = "{0}_{1}".format(self.template_name_suffix,
                                             list_name)

        if self.channel:
            if self.channel.group and self.channel.parent:
                templates.append('{0}/{1}/{2}.html'.format(
                    domain_folder,
                    self.channel.parent.long_slug,
                    list_fullname))

                if self.request.GET.get('page') and\
                   self.__class__.__name__ not in\
                   settings.OPPS_PAGINATE_NOT_APP:
                    templates.append('{0}/{1}/{2}_paginated.html'.format(
                        domain_folder, self.channel.parent.long_slug,
                        list_fullname))

            if self.request.GET.get('page') and\
               self.__class__.__name__ not in settings.OPPS_PAGINATE_NOT_APP:
                templates.append('{0}/{1}/{2}_paginated.html'.format(
                    domain_folder, self.channel.long_slug, list_fullname))

            templates.append('{0}/{1}/{2}.html'.format(
                domain_folder, self.channel.long_slug, list_fullname))

            for t in self.channel.get_ancestors()[::-1]:
                templates.append('{0}/{1}/{2}.html'.format(
                    domain_folder, t.long_slug, list_fullname))
                if self.request.GET.get('page') and\
                   self.__class__.__name__ not in\
                   settings.OPPS_PAGINATE_NOT_APP:
                    templates.append('{0}/{1}/{2}_paginated.html'.format(
                        domain_folder, t.long_slug, list_fullname))

        if self.request.GET.get('page') and\
           self.__class__.__name__ not in settings.OPPS_PAGINATE_NOT_APP:
            templates.append('{0}/{1}_paginated.html'.format(domain_folder,
                                                             list_fullname))

        templates.append('{0}/{1}/{2}.html'.format(
            self.model._meta.app_label,
            self.model._meta.module_name,
            list_name))

        return templates

    def get_template_names(self):
        domain_folder = self.get_template_folder()
        template_list = self.get_template_list(domain_folder)

        return template_list

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
