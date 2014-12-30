# -*- encoding: utf-8 -*-
from haystack.views import SearchView
from haystack.query import SearchQuerySet

from importlib import import_module

from django.conf import settings

from opps.articles.models import Post, Album


CLASSES = {
    'album': Album,
    'post': Post,
}

OPPS_HAYSTACK_APPS = getattr(
    settings, 'OPPS_HAYSTACK_APPS', {})

# Opps thirdy-apps
for app in OPPS_HAYSTACK_APPS.keys():
    if app:
        try:
            _import = OPPS_HAYSTACK_APPS[app].split('.')[-1]
            _from = u".".join(OPPS_HAYSTACK_APPS[app].split('.')[:-1])
            CLASSES[app] = getattr(
                __import__(_from, fromlist=[_import]), _import)

        except ImportError:
            pass
    else:
        CLASSES.pop(app)


class SearchOrdered(SearchView):

    __name__ = 'SearchOrdered'

    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}

        if self.searchqueryset is None:
            sqs = SearchQuerySet().filter(
                text=self.request.GET.get('q', '')
            ).order_by('-date_available', '-date')

            model = self.request.GET.get('type')
            if model:
                # get class
                sqs = sqs.models(CLASSES[model])

            form_kwargs['searchqueryset'] = sqs

        return super(SearchOrdered, self).build_form(form_kwargs)
