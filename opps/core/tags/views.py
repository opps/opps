# -*- encoding: utf-8 -*-
from django.utils import timezone
from django.contrib.sites.models import get_current_site
from django.conf import settings

from haystack.query import SearchQuerySet

from opps.views.generic.list import ListView
from opps.containers.models import Container

from opps.channels.models import Channel

from .models import Tag

USE_HAYSTACK = getattr(settings, 'OPPS_TAGS_USE_HAYSTACK', False)


class TagList(ListView):
    model = Container

    def get_template_list(self, domain_folder="containers"):
        templates = []

        list_name = 'list_tags'

        if self.request.GET.get('page') and\
           self.__class__.__name__ not in settings.OPPS_PAGINATE_NOT_APP:
            templates.append('{0}/{1}_paginated.html'.format(domain_folder,
                                                             list_name))

        templates.append('{0}/{1}.html'.format(domain_folder, list_name))
        return templates

    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        site = get_current_site(self.request)
        context['channel'] = Channel.objects.get_homepage(site)
        return context

    def get_queryset(self):
        self.site = get_current_site(self.request)
        # without the long_slug, the queryset will cause an error
        self.long_slug = 'tags'
        self.tag = self.kwargs['tag']

        if USE_HAYSTACK:
            return self.get_queryset_from_haystack()
        return self.get_queryset_from_db()

    def get_queryset_from_haystack(self):
        models = Container.get_children_models()
        sqs = SearchQuerySet().models(*models).filter(
            tags=self.tag).order_by('-date_available')
        sqs.model = Container
        return sqs

    def get_queryset_from_db(self):

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

        return self.containers
