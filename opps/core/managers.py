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

