# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone


class PublishableManager(models.Manager):

    def all_published(self):
        return super(PublishableManager, self).get_query_set().filter(
            date_available__lte=timezone.now(), published=True)
