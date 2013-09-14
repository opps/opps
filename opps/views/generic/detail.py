#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView as DjangoDetailView
from django.contrib.sites.models import get_current_site
from django.http import HttpResponseRedirect
from django.utils import timezone

from opps.views.generic.base import View


class DetailView(View, DjangoDetailView):

    def get_template_names(self):
        templates = []
        domain_folder = self.get_template_folder()
        child_class = self.object.child_class.lower()

        templates.append('{}/{}/{}/{}/detail.html'.format(
            domain_folder, child_class, self.long_slug, self.slug))
        templates.append('{}/{}/{}/detail.html'.format(
            domain_folder, self.long_slug, self.slug))

        templates.append('{}/{}/{}/detail.html'.format(
            domain_folder, child_class, self.long_slug))
        templates.append('{}/{}/detail.html'.format(domain_folder,
                                                    self.long_slug))

        templates.append('{}/{}/detail.html'.format(domain_folder,
                                                    child_class))
        templates.append('{}/detail.html'.format(domain_folder))

        return templates

    def render_to_response(self, context):
        if self.get_object().child_class == 'Link':
            return HttpResponseRedirect(self.get_object().url)
        return super(DetailView, self).render_to_response(context)

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
