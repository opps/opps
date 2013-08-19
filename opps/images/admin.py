# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.contrib.admin import SimpleListFilter

from .models import Image
from .forms import ImageModelForm
from .generate import image_url

from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules

User = get_user_model()


class UserListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _(u'User')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        # filter only users with images
        users_id = Image.objects.values_list('user_id', flat=True)

        qs = User.objects.filter(pk__in=users_id)
        if qs:
            return set([(item.username,
                         u"{0} ({1})".format(item.get_full_name(), item.email))
                       for item in qs])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == "nouser":
            queryset = queryset.filter(user__isnull=True)
        elif self.value():
            queryset = queryset.filter(user__username=self.value())

        return queryset


@apply_opps_rules('images')
class ImagesAdmin(PublishableAdmin):
    form = ImageModelForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['image_thumb', 'image_dimension', 'title',
                    'date_available', 'published']
    list_filter = [UserListFilter, 'date_available', 'published']
    search_fields = ['title']
    raw_id_fields = ['source']
    readonly_fields = ['image_thumb']
    exclude = ('user',)

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'image', 'image_thumb')}),
        (_(u'Crop'), {
            'fields': ('flip', 'flop', 'halign', 'valign', 'fit_in',
                       'smart', 'crop_x1', 'crop_x2', 'crop_y1', 'crop_y2',
                       'crop_example')}),
        (_(u'Content'), {
            'fields': ('description', 'tags', 'source')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def save_model(self, request, obj, form, change):

        if not change and len(form.more_image()) >= 1:
            [Image.objects.create(
                site=get_current_site(request),
                image=img,
                title=obj.title,
                slug=u"{0}-{1}".format(obj.slug, i),
                description=obj.description,
                published=obj.published,
                user=User.objects.get(pk=request.user.pk),
                source=obj.source
            ) for i, img in enumerate(form.more_image(), 1)]

        super(ImagesAdmin, self).save_model(request, obj, form, change)

    def get_list_display(self, request):
            list_display = self.list_display
            pop = request.GET.get('pop')
            if pop == 'oppseditor':
                list_display = ['opps_editor_select'] + list(list_display)
            return list_display

    def opps_editor_select(self, obj):
        return '''
        <a href="#" onclick="top.opps_editor_popup_selector('{0}')">{1}</a>
        '''.format(image_url(obj.image.url),
                   'Select')
    opps_editor_select.short_description = _(u'Select')
    opps_editor_select.allow_tags = True

    def image_thumb(self, obj):
        if obj.image:
            html = (u'<img width="60px" height="60px" id="imageExample" '
                    u'src="{0}" data-original="{1}" />')
            return html.format(
                image_url(obj.image.url, width=60, height=60),
                obj.image.url
            )
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True

    def image_dimension(self, obj):
        try:
            return "{0}x{1}".format(obj.image.width, obj.image.height)
        except:
            return ''
    image_dimension.short_description = _(u'Dimension')

admin.site.register(Image, ImagesAdmin)
