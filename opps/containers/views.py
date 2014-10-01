# -*- coding: utf-8 -*-

from haystack.views import SearchView

from opps.containers.models import Container
from opps.views.generic.list import ListView
from opps.views.generic.detail import DetailView


class ContainerList(ListView):
    model = Container


class ContainerDetail(DetailView):
    model = Container


class Search(SearchView):
    def get_results(self):
        return self.form.search().order_by('-date_available')
