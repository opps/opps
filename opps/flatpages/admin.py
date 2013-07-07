# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.conf import settings

from redactor.widgets import RedactorEditor

from .models import FlatPage
from opps.core.admin import apply_opps_rules
from opps.images.generate import image_url


class FlatPageAdminForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        widgets = {'content': RedactorEditor()}


@apply_opps_rules('flatpages')
class FlatPageAdmin(admin.ModelAdmin):
    form = FlatPageAdminForm
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ['get_http_absolute_url', 'short_url', 'image_thumb']
    list_display = ['title', 'site', 'published', 'date_available']
    raw_id_fields = ['main_image', 'channel']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url')}),
        (_(u'Content'), {
            'fields': ('headline', 'content', ('main_image', 'image_thumb'))}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('channel', 'published', 'date_available')}),
    )

    def image_thumb(self, obj):
        if obj.main_image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.main_image.archive.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'pk', None) is None:
            obj.user = get_user_model().objects.get(pk=request.user.pk)
            obj.site = Site.objects.get(pk=settings.SITE_ID)
        obj.save()

admin.site.register(FlatPage, FlatPageAdmin)
