# -*- encoding: utf-8 -*-
from haystack.views import SearchView
from haystack.query import SearchQuerySet

from opps.articles.models import Post, Album
from opps.multimedias.models import Audio, Video
from opps.polls.models import Poll
from opps.blogs.models import BlogPost


CLASSES = {
    'video': Video,
    'album': Album,
    'audio': Audio,
    'post': Post,
    'pool': Poll,
    'blog': BlogPost
}


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
