# -*- encoding: utf-8 -*-
from django.utils import timezone
from django.contrib.sites.models import get_current_site
from django.core.cache import cache
from django.conf import settings
from django.utils.text import slugify

from opps.views.generic.list import ListView
from opps.containers.models import Container

from .models import Tag


class TagList(ListView):
    model = Container
    template_name_suffix = '_tags'

    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context

    def get_queryset(self):
        self.site = get_current_site(self.request)
        # without the long_slug, the queryset will cause an error
        self.long_slug = 'tags'
        self.tag = self.kwargs['tag']

        cache_key = u'taglist-{}'.format(slugify(self.tag))
        if cache.get(cache_key):
            return cache.get(cache_key)

        tags = Tag.objects.filter(slug=self.tag).values_list('name') or []
        tags_names = []
        if tags:
            tags_names = [i[0] for i in tags]

        ids = []
        for tag in tags_names:
            result = self.containers = self.model.objects.filter(
                site_domain=self.site,
                tags__contains=tag,
                date_available__lte=timezone.now(),
                published=True
            )
            if result.exists():
                ids.extend([i.id for i in result])

        # remove the repeated
        ids = list(set(ids))

        # grab the containers
        self.containers = self.model.objects.filter(id__in=ids)
        expires = getattr(settings, 'OPPS_CACHE_EXPIRE', 3600)
        cache.set(cache_key, self.containers, expires)
        return self.containers
