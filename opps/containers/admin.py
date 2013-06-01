# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

from .models import Container, ContainerSource, ContainerImage
from .models import ContainerBox, ContainerBoxContainers
from opps.core.admin import PublishableAdmin, apply_opps_rules, BaseBoxAdmin
from opps.core.admin import ChannelListFilter, ContainerConfig
from opps.images.generate import image_url


@apply_opps_rules('containers')
class ContainerImageInline(admin.TabularInline):
    model = ContainerImage
    fk_name = 'container'
    raw_id_fields = ['image']
    actions = None
    extra = 1
    verbose_name = _(u"Container image")
    verbose_name_plural = _(u"Container images")
    fieldsets = [(None, {'fields': ('image', 'image_thumb', 'order')})]
    ordering = ('order',)
    readonly_fields = ['image_thumb']

    def image_thumb(self, obj):
        if obj.image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.image.image.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True


@apply_opps_rules('containers')
class ContainerSourceInline(admin.TabularInline):
    model = ContainerSource
    fk_name = 'container'
    raw_id_fields = ['source']
    actions = None
    extra = 1
    verbose_name = _(u"Container source")
    verbose_name_plural = _(u"Container sources")
    ordering = ('order',)
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('source', 'order')})]


@apply_opps_rules('containers')
class ContainerBoxContainersInline(admin.TabularInline):
    model = ContainerBoxContainers
    fk_name = 'containerbox'
    raw_id_fields = ['container']
    actions = None
    ordering = ('order',)
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('container', 'order', 'date_available', 'date_end')})]


@apply_opps_rules('containers')
class ContainerAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ['get_http_absolute_url', 'short_url',
                       'in_articleboxes', 'image_thumb']
    raw_id_fields = ['main_image', 'channel']

    def get_list_filter(self, request):
        list_filter = super(ContainerAdmin, self).list_filter
        list_filter = [ChannelListFilter] + list(list_filter)
        return list_filter


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
    raw_id_fields = ['channel', 'container', 'queryset']
    # list_display = ['name', 'channel_name', 'date_available',
    #                 'is_dynamic', 'published']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug', 'title')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'container', 'queryset')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def clean_ended_entries(self, request, queryset):
        now = timezone.now()
        for box in queryset:
            ended = box.articleboxarticles_articleboxes.filter(
                date_end__lt=now
            )
            if ended:
                ended.delete()
    clean_ended_entries.short_description = _(u'Clean ended articles')

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['name', 'channel_name', 'date_available',
                    'is_dynamic', 'published']
        else:
            return ['name', 'channel_name', 'date_available',
                    'published']

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

    list_display = ['image_thumb', 'title', 'channel_name', 'date_available',
                    'published']
    readonly_fields = ['image_thumb']

    def image_thumb(self, obj):
        if obj.main_image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.main_image.image.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True

    def get_model_perms(self, *args, **kwargs):
        return {}

    def has_add_permission(self, request):
        return False


class ContainerConfigAdmin(PublishableAdmin):
    list_display = ['key', 'key_group', 'channel', 'date_insert',
                    'date_available', 'published']
    list_filter = ["key", 'key_group', "channel", "published"]
    search_fields = ["key", "key_group", "value"]


admin.site.register(Container, HideContainerAdmin)
admin.site.register(ContainerBox, ContainerBoxAdmin)
admin.site.register(ContainerConfig, ContainerConfigAdmin)
