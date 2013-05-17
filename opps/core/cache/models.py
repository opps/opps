#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.core.cache import cache

from .managers import CacheManager, _cache_key


ModelBase = type(models.Model)


class MetaCaching(ModelBase):
    def __new__(*args, **kwargs):
        new_class = ModelBase.__new__(*args, **kwargs)
        new_manager = CacheManager()
        new_manager.contribute_to_class(new_class, 'objects')
        new_class._default_manager = new_manager
        return new_class


class Caching(models.Model):
    def save(self, *args, **kwargs):
        super(Caching, self).save()
        if kwargs.pop('invalidate_cache', True):
            cache.delete(_cache_key(self, self.id))

    class Meta:
        abstract = True

    __metaclass__ = MetaCaching
