#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings

from haystack.indexes import SearchIndex, CharField, DateTimeField
from haystack import site

from .models import Post, Album

migration_date = getattr(settings, 'MIGRATION_DATE', None)
if migration_date:
    m_date = datetime.strptime(migration_date, "%Y-%m-%d").date()
    Post.is_legacy = lambda self: m_date >= self.date_insert.date()
else:
    Post.is_legacy = lambda self: False


class PostIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    date_available = DateTimeField(model_attr='date_available')
    date_update = DateTimeField(model_attr='date_update')

    def get_updated_field(self):
        return 'date_update'

    def index_queryset(self):
        return Post.objects.filter(
            date_available__lte=datetime.now(),
            published=True)

class AlbumIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    date_available = DateTimeField(model_attr='date_available')
    date_update = DateTimeField(model_attr='date_update')

    def get_updated_field(self):
        return 'date_update'

    def index_queryset(self):
        return Album.objects.filter(
            date_available__lte=datetime.now(),
            published=True)

site.register(Post, PostIndex)
site.register(Album, AlbumIndex)
