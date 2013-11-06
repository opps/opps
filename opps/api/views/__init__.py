#!/usr/bin/env python
# -*- coding: utf-8 -*-
from opps.containers.models import Container

from .generic.list import ListView
from .generic.detail import DetailView


class ContainerAPIList(ListView):
    model = Container


class ContainerAPIDetail(DetailView):
    model = Container
