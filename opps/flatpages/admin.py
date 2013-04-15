# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.conf import settings

from redactor.widgets import RedactorEditor

from .models import FlatPage


class FlatPageAdminForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        widgets = {'content': RedactorEditor()}


class FlatPageAdmin(admin.ModelAdmin):
    form = FlatPageAdminForm
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ['get_http_absolute_url', 'short_url']
    list_display = ['title', 'site', 'published', 'date_available']
    raw_id_fields = ['main_image']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url')}),
        (_(u'Content'), {
            'fields': ('headline', 'content', 'main_image')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'pk', None) is None:
            obj.user = get_user_model().objects.get(pk=request.user.pk)
            obj.site = Site.objects.get(pk=settings.SITE_ID)
        obj.save()

admin.site.register(FlatPage, FlatPageAdmin)
