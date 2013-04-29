# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site

from django_thumbor import generate_url

from .models import Image
from .forms import ImageModelForm
from opps.core.admin import PublishableAdmin


class ImagesAdmin(PublishableAdmin):
    form = ImageModelForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['image_thumb', 'title', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    search_fields = ['title']
    raw_id_fields = ['source']
    readonly_fields = ['image_thumb']
    exclude = ('user',)

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'image')}),
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
                user=get_user_model().objects.get(pk=request.user.pk))
                for i, img in enumerate(form.more_image(), 1)]
        super(ImagesAdmin, self).save_model(request, obj, form, change)

    def image_thumb(self, obj):
        if obj.image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                generate_url(obj.image.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True

admin.site.register(Image, ImagesAdmin)
