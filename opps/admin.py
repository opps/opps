#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.admin import *
from django.conf import settings

OPPS_ADMIN = getattr(settings, 'OPPS_ADMIN', "Admin") 

def verify_opps_local_admin(func):
    def register_local(self, model_or_iterable, admin_class=None, **options):
        # XXX: usar import lib para ter arquivos separados de admin se for necessário
        import opps.local_admin
        new_admin_class_name = "%s%s" % (model_or_iterable.__name__, OPPS_ADMIN)
        new_admin_class =  testeopps.opps.admin.__dict__.get(new_admin_class_name) or admin_class
        return func(self, model_or_iterable=model_or_iterable, admin_class=new_admin_class, options=options)
    return register_local

decorated_register = verify_opps_local_admin(AdminSite.register)
AdminSite.register = decorated_register
