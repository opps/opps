#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView as DjangoDetailView
from django.contrib.sites.models import Site, get_current_site
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.conf import settings
from opps.views.generic.base import View


class DetailView(View, DjangoDetailView):

    def get_template_list(self, domain_folder="containers"):
        child_class = self.object.child_class.lower()

        templates = ['{0}/{1}/{2}/detail.html'.format(
            domain_folder, self.long_slug, self.slug)]

        all_long_slug = [i.long_slug for i in self.channel.get_ancestors()]
        all_long_slug.append(self.long_slug)
        for l in all_long_slug[::-1]:
            templates.append('{0}/{1}/{2}_detail.html'.format(
                domain_folder, l, child_class))
        templates.append('{0}/{1}_detail.html'.format(domain_folder,
                                                      child_class))

        for l in all_long_slug[::-1]:
            templates.append('{0}/{1}/detail.html'.format(domain_folder, l))
        templates.append('{0}/detail.html'.format(domain_folder))

        return templates

    def get_template_names(self):
        if self.template_name:
            return [self.template_name]

        domain_folder = self.get_template_folder()
        template_list = self.get_template_list(domain_folder)

        if domain_folder != "containers":
            template_list.extend(self.get_template_list())

        return template_list

    def render_to_response(self, context):
        if self.get_object().child_class == 'Link':
            return HttpResponseRedirect(self.get_object().url)
        return super(DetailView, self).render_to_response(context)

    def get_queryset(self):
        self.fallback = getattr(settings, 'OPPS_MULTISITE_FALLBACK', False)
        self.site = get_current_site(self.request)
        self.site_master = Site.objects.order_by('id')[0]
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

        qs = queryset.filter(**filters)._clone()
        if not qs and self.fallback and self.site_master != self.site:
            filters['site_domain'] = self.site_master.domain
            qs = queryset.filter(**filters)._clone()
        return qs
