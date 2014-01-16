#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import QuerySet
from .forms import QuerySetAdminForm
from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules


@apply_opps_rules('boxes')
class QuerySetAdmin(PublishableAdmin):
    form = QuerySetAdminForm
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    raw_id_fields = ['channel']
    readonly_fields = ['data_sample']
    exclude = ('user',)

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Rules'), {
            'fields': ('model', 'order', 'offset', 'limit', 'channel',
                       'filters')}),
        (_(u'Publication'), {
            'classes': ('extrapretty',),
            'fields': ('published', 'date_available')}),
        (_(u'Data sample'), {
            'classes': ('extrapretty',),
            'fields': ('data_sample',)}),
    )

    def data_sample(self, obj):
        html = []

        qs = obj.get_queryset().all()
        count = qs.count()
        if count:
            html.append('<strong>Items:</strong> {0}<ul>'.format(count))
            for item in qs:
                html.append("<li>{0}</li>".format(item))
            html.append('</ul>')
        else:
            html.append('<ul><li>No data</li></ul>')

        return u''.join(html)
    data_sample.short_description = _(u'Data sample')
    data_sample.allow_tags = True


admin.site.register(QuerySet, QuerySetAdmin)
