# -*- encoding: utf-8 -*-
from haystack.views import SearchView
from haystack.query import SearchQuerySet

from opps.articles.models import Post, Album


CLASSES = {
    'album': Album,
    'post': Post,
}

# Opps thirdy-apps
try:
    from opps.multimedias.models import Audio, Video

    CLASSES.update({
        'video': Video,
        'audio': Audio
    })
except ImportError:
    pass

try:
    from opps.polls.models import Poll

    CLASSES.update({'pool': Poll})
except ImportError:
    pass

try:
    from opps.blogs.models import BlogPost

    CLASSES.update({'blog': BlogPost})
except ImportError:
    pass


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
