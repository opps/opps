#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.core.cache import cache
from django.conf import settings


def _cache_key(model, id):
    return u'{}:{}:{}'.format(settings.CACHE_PREFIX,
                              model._meta.db_table,
                              id)


class CacheManager(models.Manager):
    def get(self, *args, **kwargs):
        id = repr(kwargs)
        pointer_key = _cache_key(self.model, id)
        model_key = cache.get(pointer_key)

        if model_key is not None:
            model = cache.get(model_key)
            if model is not None:
                return model

        model = super(CacheManager, self).get(*args, **kwargs)

        if not model_key:
            model_key = _cache_key(model, model.pk)
            cache.set(pointer_key, model_key, settings.CACHE_EXPIRE)

        cache.set(model_key, model, settings.CACHE_EXPIRE)
        return model
