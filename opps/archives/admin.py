# coding: utf-8
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from opps.core.admin import apply_opps_rules
from opps.core.permissions.admin import AdminViewPermission

from .models import File


@apply_opps_rules('archives')
class FileAdmin(AdminViewPermission):
    search_fields = ['title', 'slug']
    raw_id_fields = ['user']
    list_display = ['title', 'slug', 'download_link', 'published']
    ordering = ('-date_available',)
    list_filter = ['date_available', 'published']
    prepopulated_fields = {"slug": ["title"]}

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug',)}),
        (_(u'Content'), {
            'fields': ('description', 'archive', 'archive_link', 'tags')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',)}),
    )

    def download_link(self, obj):
        download_url = ''
        if obj.archive:
            download_url = obj.archive.url
        elif obj.archive_link:
            download_url = obj.archive_link

        html = '<a href="{0}">{1}</a>'.format(
            download_url,
            unicode(_(u'Download')))
        return html
    download_link.short_description = _(u'download')
    download_link.allow_tags = True

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = get_user_model().objects.get(pk=request.user.pk)
            obj.date_insert = timezone.now()
        obj.date_update = timezone.now()
        obj.save()

admin.site.register(File, FileAdmin)
