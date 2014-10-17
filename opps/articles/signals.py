#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.redirects.models import Redirect


def redirect_generate(sender, instance, created, **kwargs):
    obj, create = Redirect.objects.get_or_create(
        old_path=instance.get_absolute_url(),
        site=instance.site)
    obj.new_path = instance.url
    obj.save()
