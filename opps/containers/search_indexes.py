# -*- coding: utf-8 -*-

from haystack.indexes import \
    CharField, DateTimeField, MultiValueField, SearchIndex, IntegerField


class ContainerIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    channel_id = IntegerField(model_attr="channel_id")
    date_available = DateTimeField(model_attr='date_available')
    date_update = DateTimeField(model_attr='date_update')
    tags = MultiValueField(null=True)

    def prepare_tags(self, obj):
        if not obj.tags:
            return
        tags = []
        for tag in obj.get_tags() or []:
            tags.append(tag.slug)
            tags.append(tag.name)
        return tags

    def get_updated_field(self):
        return 'date_update'

    def index_queryset(self, using=None):
        return self.get_model().objects.all_published()
