# -*- encoding: utf-8 -*-
from django.utils import timezone
from django.contrib.sites.models import get_current_site

from opps.views.generic.list import ListView
from opps.containers.models import Container


class TagList(ListView):
    model = Container
    template_name_suffix = '_tags'

    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context

    def get_queryset(self):
        self.site = get_current_site(self.request)
        self.long_slug= self.kwargs['tag']
        self.containers = self.model.objects.filter(
            site_domain=self.site,
            tags__icontains=self.long_slug,
            date_available__lte=timezone.now(),
            published=True).all()
        return self.containers
