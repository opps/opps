# -*- coding: utf-8 -*-

from datetime import datetime

from django.conf import settings

from haystack.indexes import Indexable

from opps.containers.search_indexes import ContainerIndex

from .models import Post, Album, Link


migration_date = getattr(settings, 'MIGRATION_DATE', None)
if migration_date:
    m_date = datetime.strptime(migration_date, "%Y-%m-%d").date()
    Post.is_legacy = lambda self: m_date >= self.date_insert.date()
else:
    Post.is_legacy = lambda self: False


class PostIndex(ContainerIndex, Indexable):

    def get_model(self):
        return Post


class AlbumIndex(ContainerIndex, Indexable):
    def get_model(self):
        return Album


class LinkIndex(ContainerIndex, Indexable):

    def get_model(self):
        return Link
