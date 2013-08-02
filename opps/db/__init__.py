#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .conf import settings


def Db(*args, **kwarg):
    _import = settings.OPPS_DB_ENGINE.split('.')[-1]
    _from = u".".join(settings.OPPS_DB_ENGINE.split('.')[:-1])
    call = getattr(__import__(_from, fromlist=[_import]), _import)
    return call(*args)
