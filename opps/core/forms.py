#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models


def model_choices():
    try:
        return tuple(sorted([
            (u"{0}.{1}".format(app._meta.app_label, app._meta.object_name),
             u"{0} - {1}".format(app._meta.app_label, app._meta.object_name))
            for app in models.get_models() if 'opps.' in app.__module__]))
    except ImportError:
        return tuple([])
