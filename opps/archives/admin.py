from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from opps.core.admin import apply_opps_rules
from opps.contrib.multisite.admin import AdminViewPermission

from .models import File


@apply_opps_rules('archives')
class FileAdmin(AdminViewPermission):
    search_fields = ['title', 'slug']
    raw_id_fields = ['user']
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

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = get_user_model().objects.get(pk=request.user.pk)
            obj.date_insert = timezone.now()
        obj.date_update = timezone.now()
        obj.save()

admin.site.register(File, FileAdmin)
