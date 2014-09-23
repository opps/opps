# -*- coding: utf-8 -*-

from django.db.models import Manager
from django.db import models
from django.utils import timezone


class PublishableQuerySet(models.query.QuerySet):

    def all_published(self):
        return self.filter(**self.get_all_published_lookups())

    def get_all_published_lookups(self, prefix=""):
        return {
            '%sdate_available__lte' % prefix: timezone.now(),
            '%spublished' % prefix: True,
        }


class PublishableManager(Manager):
    queryset_class = PublishableQuerySet

    def get_query_set(self):
        return self.queryset_class(self.model)

    def all_published(self):
        return self.get_query_set().all_published()

    def get_all_published_lookups(self, prefix=""):
        return self.get_query_set().get_all_published_lookups(prefix)
