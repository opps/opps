# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db.models import Manager


class PublishableManager(Manager):

    def all_published(self):
        return super(PublishableManager, self).get_query_set().filter(
            date_available__lte=timezone.now(), published=True)
