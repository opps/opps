# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.contrib.admin import SimpleListFilter
from django.utils.text import slugify
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.db import transaction

from .models import Image
from .forms import ImageModelForm
from .generate import image_url

from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules
from opps.articles.models import Post, Album, ArticleImage
from opps.channels.models import Channel

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
        qs = User.objects.filter(image__isnull=False).distinct()
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
            'fields': ('site', 'title', 'slug', 'image', 'generate_article')}),
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

        images = []
        if not change and len(form.more_image()) >= 1:
            images = [
                Image.objects.create(
                    site=get_current_site(request),
                    image=img,
                    title=obj.title,
                    slug=u"{0}-{1}".format(obj.slug, i),
                    description=obj.description,
                    published=obj.published,
                    user=User.objects.get(pk=request.user.pk),
                    source=obj.source
                )
                for i, img in enumerate(form.more_image(), 1)
            ]

        super(ImagesAdmin, self).save_model(request, obj, form, change)

        if not change:
            self.generate_article(request, obj, change, images)

    @transaction.commit_on_success
    def generate_article(self, request, obj, change, images):

        generate_article = False
        article_type = request.POST.get('generate_article_type')
        if article_type in ('Post', 'Album'):
            channel_id = request.POST.get('generate_article_channel')
            try:
                article_channel = Channel.objects.get(pk=int(channel_id))
            except:
                article_channel = Channel.objects.get_homepage(site=obj.site)

            article_title = request.POST.get('generate_article_title')
            article_slug = slugify(article_title)

            if article_type == 'Post':
                article_model = Post
            elif article_type == 'Album':
                article_model = Album

            if article_model.objects.filter(slug=article_slug,
                                            channel=article_channel).exists():
                article_slug += "-{}".format(obj.slug)

            generate_article = True

        tags = request.POST.get('tags')
        if tags:
            tags = tags.replace('"', '')
            for img in images:
                img.tags.add(*tags.split(','))
                img.save()

        if generate_article:
            article = article_model.objects.create(
                title=article_title,
                slug=article_slug,
                channel=article_channel,
                published=False,
                site=obj.site,
                user=obj.user,
                main_image=obj
            )

            images.insert(0, obj)

            for i, image in enumerate(images):
                ArticleImage.objects.create(
                    article=article,
                    image=image,
                    order=i
                )

            inf = (article._meta.app_label, article._meta.module_name)
            admin_url = reverse("admin:%s_%s_change" % inf, args=(article.pk,))

            msg = _(
                u"New {type} created: "
                u"<a href='{url}' target='_blank'>{title}</a>"
            ).format(
                type=_(article_type),
                url=admin_url,
                title=article.title
            )

            messages.info(request, mark_safe(msg), extra_tags='safe')

    def image_thumb(self, obj):
        if obj.image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.image.url, width=60, height=60))
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
