#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from opps.core.admin import PublishableAdmin, apply_opps_rules, BaseBoxAdmin
from opps.core.permissions.admin import AdminViewPermission
from opps.core.filters import ChannelListFilter, HasQuerySet
from opps.images.generate import image_url
from opps.fields.models import Field, FieldOption

from .models import Container, ContainerImage, Mirror
from .models import ContainerBox, ContainerBoxContainers, ContainerRelated
from .forms import ContainerBoxContainersInlineForm, ContainerImageInlineForm


@apply_opps_rules('containers')
class ContainerRelatedInline(admin.TabularInline):
    model = ContainerRelated
    fk_name = 'container'
    raw_id_fields = ['related']
    actions = None
    ordering = ('order',)
    extra = 1
    classes = ('collapse',)
    verbose_name = _(u'Related content')
    verbose_name_plural = _(u'Related contents')


@apply_opps_rules('containers')
class ContainerImageInline(admin.TabularInline):
    model = ContainerImage
    form = ContainerImageInlineForm
    fk_name = 'container'
    raw_id_fields = ['image']
    sortable_field_name = "order"
    actions = None
    extra = 0
    verbose_name = _(u"Image")
    verbose_name_plural = _(u"Images")
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
    form = ContainerBoxContainersInlineForm
    fk_name = 'containerbox'
    raw_id_fields = ['container', 'main_image']
    sortable_field_name = "order"
    actions = None
    ordering = ('order',)
    extra = 0
    fieldsets = [(None, {
        'fields': ('container', 'aggregate', 'highlight', 'order',
                   'date_available', 'date_end', 'hat', 'title',
                   'main_image', 'main_image_caption', 'url', 'url_target')})]


@apply_opps_rules('containers')
class ContainerAdmin(PublishableAdmin, AdminViewPermission):
    inlines = [ContainerRelatedInline]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ['get_http_absolute_url', 'short_url',
                       'in_containerboxes', 'image_thumb']
    raw_id_fields = ['main_image', 'channel', 'mirror_channel']
    ordering = ('-date_available',)

    autocomplete_lookup_fields = {
        'fk': ['channel'],
    }

    def get_list_filter(self, request):
        list_filter = super(ContainerAdmin, self).list_filter
        list_filter = [ChannelListFilter] + list(list_filter)
        return list_filter

    def save_model(self, request, obj, form, change):
        super(ContainerAdmin, self).save_model(request, obj, form, change)
        _json = {}
        for field in Field.objects.filter(
                application__contains=obj.__class__.__name__):
            if field.type == 'checkbox':
                for fo in FieldOption.objects.filter(field=field):
                    key = "{0}_{1}".format(field.slug, fo.option.slug)
                    _json[key] = request.POST.get('json_{0}'.format(key), '')
            else:
                _json[field.slug] = request.POST.get(
                    'json_{0}'.format(field.slug), '')

        obj.json = json.dumps(_json)
        obj.save()


@apply_opps_rules('containers')
class ContainerBoxAdmin(BaseBoxAdmin, AdminViewPermission):
    inlines = [ContainerBoxContainersInline]
    raw_id_fields = ['channel', 'queryset', 'main_image']
    list_display = ['name', 'site', 'channel_name', 'date_available',
                    'published']
    save_as = True

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug', 'title', 'title_url',
                       'main_image', 'main_image_caption')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'queryset')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('content_group', 'published', 'date_available')}),
    )

    autocomplete_lookup_fields = {
        'fk': ['channel'],
    }

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


class HideContainerAdmin(PublishableAdmin, AdminViewPermission):

    list_display = ['image_thumb', 'get_child_class', 'title', 'channel_name',
                    'date_available', 'published']

    list_display_links = ['image_thumb', 'title']

    readonly_fields = ['image_thumb']

    def get_child_class(self, obj):
        return _(obj.child_class)
    get_child_class.short_description = _(u'Child class')
    get_child_class.admin_order_field = 'child_class'

    def get_model_perms(self, *args, **kwargs):
        return {}

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Redirects to specific child_class admin change form.
        """
        obj = self.queryset(request).get(pk=object_id)
        return redirect(reverse('admin:{}_{}_change'.format(
            obj._meta.app_label, obj._meta.module_name), args=(obj.pk,)))

    def get_list_filter(self, request):
        list_filter = super(HideContainerAdmin, self).list_filter
        list_filter = [ChannelListFilter] + list(list_filter)
        return list_filter

    def queryset(self, request):
        qs = super(HideContainerAdmin, self).queryset(request)
        # TODO: Document this
        blacklist = getattr(settings, 'OPPS_CONTAINERS_BLACKLIST', [])
        if blacklist:
            qs = qs.exclude(child_class__in=blacklist)
        return qs.select_related('main_image')


admin.site.register(Container, HideContainerAdmin)
admin.site.register(ContainerBox, ContainerBoxAdmin)
admin.site.register(Mirror, HideContainerAdmin)
