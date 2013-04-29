#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils import timezone
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class PublishableAdmin(admin.ModelAdmin):
    """
    Overrides standard admin.ModelAdmin save_model method
    It sets user (author) based on data from requet.
    """
    list_display = ['title', 'channel_name', 'date_available', 'published']
    list_filter = ['date_available', 'published', 'channel_name',
                   'child_class']
    search_fields = ['title', 'slug', 'headline', 'channel_name']
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'pk', None) is None:
            obj.user = get_user_model().objects.get(pk=request.user.pk)
            obj.date_insert = timezone.now()
            obj.site = Site.objects.get(pk=settings.SITE_ID)
        obj.date_update = timezone.now()
        obj.save()


def apply_rules(admin_class, app):
    """
    To allow overrides of admin rules for opps apps
    it uses the settings.py to load the values

    example of use:

    your project's settings.py

    OPPS_ADMIN_RULES = {
        'appname.ModelNameAdmin': {
            'fieldsets': (
                (u'Identification', {
                    'fields': ('site', 'title', 'slug')}),
            ),
            'list_display': (...),
            'list_filter': (...),
            'search_fields': (...),
            ...
        }
    }

    On appname/admin.py

    as a factory:

    from opps.core.admin import apply_rules
    ModelNameAdmin = apply_rules(ModelNameAdmin, 'appname')

    as a decorator:

    from opps.core.admin import apply_opps_rules

    @apply_opps_rules('appname')
    class ModelNameAdmin(admin.ModelAdmin):
        ...
    """

    key = "{0}.{1}".format(app, admin_class.__name__)
    OPPS_ADMIN_RULES = getattr(settings, 'OPPS_ADMIN_RULES', {})
    rules = OPPS_ADMIN_RULES.get(key)

    if not rules:
        return admin_class

    fieldsets = rules.get('fieldsets')
    if fieldsets:
        new_items = [(_(item[0]), item[1]) for item in fieldsets]
        admin_class.fieldsets = new_items

    attrs = ('list_display', 'list_filter',
             'search_fields', 'exclude', 'raw_id_fields',
             'prepopulated_fields')

    for attr in attrs:
        to_apply = rules.get(attr)
        if to_apply:
            setattr(admin_class, attr, to_apply)

    # TODO:
    # form
    # inlines
    # actions
    # override methods

    return admin_class


def apply_opps_rules(app):

    def wrap(admin_class):
        admin_class = apply_rules(admin_class, app)
        return admin_class

    return wrap

apply_opps_rules.__doc__ = apply_rules.__doc__
