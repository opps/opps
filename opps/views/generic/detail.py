#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.detail import DetailView as DjangoDetailView
from django.contrib.sites.models import get_current_site
from django.utils import timezone

from opps.views.generic.base import View


class DetailView(View, DjangoDetailView):

    def get_template_names(self):
        names = []
        domain_folder = self.get_template_folder()

        names.append('{}/{}/{}.html'.format(
            domain_folder, self.long_slug, self.slug))
        names.append('{}/{}.html'.format(domain_folder, self.long_slug))

        try:
            names = names + super(DetailView, self).get_template_names()
        except ImproperlyConfigured:
            pass

        return names

    @property
    def queryset(self):
        self.site = get_current_site(self.request).domain
        self.slug = self.kwargs.get('slug')
        self.long_slug = self.get_long_slug()
        if not self.long_slug:
            return None

        self.set_channel_rules()

        filters = dict(
            site_domain=self.site,
            channel_long_slug=self.long_slug,
            slug=self.slug
        )

        preview_enabled = self.request.user and self.request.user.is_staff

        if not preview_enabled:
            filters['date_available__lte'] = timezone.now()
            filters['published'] = True

        self.article = self.model.objects.filter(
            **filters
        )

        return self.article._clone()
