#!/usr/bin/env python
# -*- coding: utf-8 -*-
from haystack.indexes import SearchIndex, Indexable, CharField, DateTimeField
from haystack.indexes import BooleanField

from .models import Channel


class ChannelIndex(SearchIndex, Indexable):
    text = CharField(document=True, use_template=True)
    date_available = DateTimeField(model_attr='date_available')
    date_update = DateTimeField(model_attr='date_update')
    published = BooleanField(model_attr='published')

    def get_updated_field(self):
        return 'date_update'

    def get_model(self):
        return Channel
