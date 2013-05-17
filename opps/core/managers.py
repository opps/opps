#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings


class PublishableManager(models.Manager):
    def all_published(self):
        return super(PublishableManager, self).get_query_set().filter(
            date_available__lte=timezone.now(), published=True)


class CacheManager(models.Manager):
    def __cache_key(self, id):
        return u'{}:{}:{}'.format(settings.CACHE_PREFIX,
                                  self.model._meta.db_table,
                                  id)

    def get(self, *args, **kwargs):
        id = repr(kwargs)
        pointer_key = self.__cache_key(id)
        model_key = cache.get(pointer_key)

        if model_key is not None:
            model = cache.get(model_key)
            if model is not None:
                return model

        model = super(CacheManager, self).get(*args, **kwargs)

        if not model_key:
            model_key = self.__cache_key(model, model.pk)
            cache.set(pointer_key, model_key, settings.CACHE_EXPIRE)

        cache.set(model_key, model, settings.CACHE_EXPIRE)
        return model
