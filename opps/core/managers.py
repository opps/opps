# -*- coding: utf-8 -*-

from django.utils import timezone
from django.db.models import Manager


class PublishableManager(Manager):

    def all_published(self):
        return super(PublishableManager, self).get_query_set().filter(
            **self.get_all_published_lookups())

    def get_all_published_lookups(self, prefix=""):
        return {
            '%sdate_available__lte' % prefix: timezone.now(),
            '%spublished' % prefix: True,
        }
