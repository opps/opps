# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

from .models import Post, Album, Article, Link, ArticleSource, ArticleImage
from .models import (ArticleBox, ArticleBoxArticles, ArticleConfig,
                     PostRelated, AlbumRelated)
from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules
from opps.core.admin import BaseBoxAdmin
from opps.core.admin import ChannelListFilter
from opps.images.generate import image_url

from redactor.widgets import RedactorEditor


@apply_opps_rules('articles')
class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    fk_name = 'article'
    raw_id_fields = ['image']
    actions = None
    extra = 1
    fieldsets = [(None, {'fields': ('image', 'image_thumb',
                         'order', 'caption')})]
    ordering = ('order',)
    readonly_fields = ['image_thumb']

    def image_thumb(self, obj):
        if obj.image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.image.image.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True


@apply_opps_rules('articles')
class ArticleSourceInline(admin.TabularInline):
    model = ArticleSource
    fk_name = 'article'
    raw_id_fields = ['source']
    actions = None
    extra = 1
    ordering = ('order',)
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('source', 'order')})]


@apply_opps_rules('articles')
class ArticleBoxArticlesInline(admin.TabularInline):
    model = ArticleBoxArticles
    fk_name = 'articlebox'
    raw_id_fields = ['article']
    actions = None
    ordering = ('order',)
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('article', 'order', 'date_available', 'date_end')})]


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'content': RedactorEditor()}


@apply_opps_rules('articles')
class ArticleAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ['get_http_absolute_url', 'short_url',
                       'in_articleboxes', 'image_thumb']
    raw_id_fields = ['main_image', 'channel']

    def get_list_filter(self, request):
        list_filter = super(ArticleAdmin, self).list_filter
        list_filter = [ChannelListFilter] + list(list_filter)
        return list_filter


@apply_opps_rules('articles')
class PostRelatedInline(admin.TabularInline):
    model = PostRelated
    fk_name = 'post'
    raw_id_fields = ['related']
    actions = None
    ordering = ('order',)
    extra = 1
    classes = ('collapse',)


@apply_opps_rules('articles')
class AlbumRelatedInline(admin.TabularInline):
    model = AlbumRelated
    fk_name = 'album'
    raw_id_fields = ['related']
    actions = None
    ordering = ('order',)
    extra = 1
    classes = ('collapse',)


@apply_opps_rules('articles')
class PostAdmin(ArticleAdmin):
    form = PostAdminForm
    inlines = [ArticleImageInline, ArticleSourceInline, PostRelatedInline]
    raw_id_fields = ['main_image', 'channel', 'albums']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url')}),
        (_(u'Content'), {
            'fields': ('hat', 'short_title', 'headline', 'content',
                       ('main_image', 'image_thumb'), 'main_image_caption',
                       'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'albums',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel', 'in_articleboxes')}),
    )


class AlbumAdminForm(forms.ModelForm):
    class Meta:
        model = Album
        widgets = {
            'headline': RedactorEditor(
                redactor_options=settings.REDACTOR_SIMPLE
            )
        }


@apply_opps_rules('articles')
class AlbumAdmin(ArticleAdmin):
    form = AlbumAdminForm
    inlines = [ArticleImageInline, ArticleSourceInline, AlbumRelatedInline]
    list_display = ['title', 'channel', 'images_count',
                    'date_available', 'published', 'preview_url']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url',)}),
        (_(u'Content'), {
            'fields': ('hat', 'short_title', 'headline',
                       ('main_image', 'image_thumb'), 'main_image_caption',
                       'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel')}),
    )


class LinkAdminForm(forms.ModelForm):
    class Meta:
        model = Link


@apply_opps_rules('articles')
class LinkAdmin(ArticleAdmin):
    form = LinkAdminForm
    raw_id_fields = ['articles', 'channel', 'main_image']
    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url',)}),
        (_(u'Content'), {
            'fields': ('hat', 'short_title', 'headline', 'url', 'articles',
                       ('main_image', 'image_thumb'), 'main_image_caption',
                       'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel')}),
    )


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


@apply_opps_rules('articles')
class ArticleBoxAdmin(BaseBoxAdmin):
    inlines = [ArticleBoxArticlesInline]
    raw_id_fields = ['channel', 'article', 'queryset']
    list_display = ['name', 'channel_name', 'date_available',
                    'published']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug', 'title')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'article', 'queryset')}),
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
        list_display = getattr(self, 'list_display', [])
        if request.user.is_superuser:
            return list_display + ['is_dynamic']
        return list_display

    def get_list_filter(self, request):
        list_filter = super(ArticleBoxAdmin, self).list_filter
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


class HideArticleAdmin(PublishableAdmin):

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

    def get_list_filter(self, request):
        list_filter = super(HideArticleAdmin, self).list_filter
        list_filter = [ChannelListFilter] + list(list_filter)
        return list_filter


class ArticleConfigAdmin(PublishableAdmin):
    list_display = ['key', 'key_group', 'channel', 'date_insert',
                    'date_available', 'published']
    list_filter = ["key", 'key_group', "channel", "published"]
    search_fields = ["key", "key_group", "value"]


admin.site.register(Article, HideArticleAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(ArticleBox, ArticleBoxAdmin)
admin.site.register(ArticleConfig, ArticleConfigAdmin)
