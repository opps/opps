#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

from .models import Container, ContainerImage
from .models import ContainerBox, ContainerBoxContainers
from opps.core.admin import PublishableAdmin, apply_opps_rules, BaseBoxAdmin
from opps.core.admin import ChannelListFilter
from opps.images.generate import image_url
from opps.fields.models import Field, FieldOption


@apply_opps_rules('containers')
class ContainerImageInline(admin.TabularInline):
    model = ContainerImage
    fk_name = 'container'
    raw_id_fields = ['image']
    sortable_field_name = "order"
    actions = None
    extra = 0
    verbose_name = _(u"Container image")
    verbose_name_plural = _(u"Container images")
    fieldsets = [(None, {'fields': ('image', 'image_thumb',
                         'order', 'caption')})]
    ordering = ('order',)
    readonly_fields = ['image_thumb']

    def image_thumb(self, obj):
        if obj.image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.image.archive.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True


@apply_opps_rules('containers')
class ContainerBoxContainersInline(admin.StackedInline):
    model = ContainerBoxContainers
    fk_name = 'containerbox'
    raw_id_fields = ['container', 'main_image']
    sortable_field_name = "order"
    actions = None
    ordering = ('order',)
    extra = 0
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('container', 'aggregate', 'order', 'date_available',
                   'date_end', 'hat', 'title', 'main_image',
                   'main_image_caption', 'url')})]


@apply_opps_rules('containers')
class ContainerAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ['get_http_absolute_url', 'short_url',
                       'in_containerboxes', 'image_thumb']
    raw_id_fields = ['main_image', 'channel']
    ordering = ('-date_available',)

    def get_list_filter(self, request):
        list_filter = super(ContainerAdmin, self).list_filter
        list_filter = [ChannelListFilter] + list(list_filter)
        return list_filter

    def save_model(self, request, obj, form, change):
        if not change:
            super(ContainerAdmin, self).save_model(request, obj, form, change)
        _json = {}
        for field in Field.objects.filter(
            application__contains=obj.__class__.__name__):
            for fo in FieldOption.objects.filter(field=field):
                key = "{}_{}".format(field.slug, fo.option.slug)
                _json[key] = request.POST.get('json_{}'.format(key), '')

        obj.json = json.dumps(_json)
        obj.save()


class HasQuerySet(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _(u'Has queryset')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'hasqueryset'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('no', _(u'No')),
            ('yes', _(u'Yes'))
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == "no":
            queryset = queryset.filter(queryset__isnull=True)
        elif self.value() == 'yes':
            queryset = queryset.filter(queryset__isnull=False)

        return queryset


@apply_opps_rules('containers')
class ContainerBoxAdmin(BaseBoxAdmin):
    inlines = [ContainerBoxContainersInline]
    raw_id_fields = ['channel', 'queryset']
    list_display = ['name', 'channel_name', 'date_available',
                    'published']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug', 'title')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'queryset')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def clean_ended_entries(self, request, queryset):
        now = timezone.now()
        for box in queryset:
            ended = box.containerboxcontainers_containerboxes.filter(
                date_end__lt=now
            )
            if ended:
                ended.delete()
    clean_ended_entries.short_description = _(u'Clean ended containers')

    def get_list_display(self, request):
        list_display = getattr(self, 'list_display', [])
        if request.user.is_superuser:
            return list_display + ['is_dynamic']
        return list_display

    def get_list_filter(self, request):
        list_filter = super(ContainerBoxAdmin, self).list_filter
        if request.user.is_superuser:
            list_filter = [HasQuerySet] + list_filter
        return list_filter

    def is_dynamic(self, obj):
        if obj.queryset:
            return True
        else:
            return False
    is_dynamic.short_description = _(u'Dynamic')
    is_dynamic.boolean = True

    actions = ('clean_ended_entries',)


class HideContainerAdmin(PublishableAdmin):

    list_display = ['image_thumb', 'child_class', 'title',
                    'channel_name', 'date_available',
                    'published']
    readonly_fields = ['image_thumb']

    def image_thumb(self, obj):
        if obj.main_image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.main_image.archive.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True

    def get_model_perms(self, *args, **kwargs):
        return {}

    def has_add_permission(self, request):
        return False


admin.site.register(Container, HideContainerAdmin)
admin.site.register(ContainerBox, ContainerBoxAdmin)
