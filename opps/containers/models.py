# -*- coding: utf-8 -*-
import json
import operator

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site

from polymorphic import PolymorphicModel
from polymorphic.showfields import ShowFieldContent

from opps.core.cache import _cache_key
from opps.core.models import Publishable, Slugged, Channeling, Imaged
from opps.core.tags.models import Tagged
from opps.db.models.fields import JSONField
from opps.boxes.models import BaseBox

from .managers import ContainerManager
from .signals import shorturl_generate, delete_container
from .tasks import check_mirror_channel, check_mirror_site


class Container(PolymorphicModel, ShowFieldContent, Publishable, Slugged,
                Channeling, Imaged, Tagged):
    title = models.CharField(_(u"Title"), max_length=140, db_index=True)
    hat = models.CharField(
        _(u"Hat"),
        max_length=140,
        null=True, blank=True,
    )
    short_url = models.URLField(
        _(u"Short URL"),
        null=True, blank=True,
    )
    child_class = models.CharField(
        _(u'Child class'),
        max_length=30,
        null=True, blank=True,
        db_index=True
    )
    child_module = models.CharField(
        _(u'Child module'),
        max_length=120,
        null=True, blank=True,
        db_index=True
    )
    child_app_label = models.CharField(
        _(u'Child app label'),
        max_length=30,
        null=True, blank=True,
        db_index=True
    )
    show_on_root_channel = models.BooleanField(
        _(u"Show on root channel?"),
        default=True
    )
    source = models.CharField(
        _('Source'),
        null=True, blank=True,
        max_length=255)
    json = JSONField(_(u"Customized"),
                     null=True, blank=True)
    related_containers = models.ManyToManyField(
        'containers.Container',
        null=True, blank=True,
        related_name='container_relatedcontainers',
        through='containers.ContainerRelated',
    )

    objects = ContainerManager()

    def __unicode__(self):
        return u"{0}".format(self.get_absolute_url())

    def __repr__(self):
        val = self.__unicode__()
        if isinstance(val, str):
            return val
        elif not isinstance(val, unicode):
            val = unicode(val)
        return val.encode('utf8')

    class Meta:
        ordering = ['-date_available']
        verbose_name = _(u'Container')
        verbose_name_plural = _(u'Containers')
        unique_together = ("site", "channel", "slug")

    def save(self, *args, **kwargs):
        if not self.channel_name:
            self.channel_name = self.channel.name
        if not self.channel_long_slug:
            self.channel_long_slug = self.channel.long_slug
        self.child_class = self.__class__.__name__
        self.child_module = self.__class__.__module__
        self.child_app_label = self._meta.app_label
        if self.slug == u"":
            self.slug = slugify(self.title)

        models.signals.post_save.connect(shorturl_generate,
                                         sender=self.__class__)
        super(Container, self).save(*args, **kwargs)
        if settings.OPPS_MIRROR_CHANNEL and (
            self.mirror_channel or self.mirror_site)\
                and self.child_class != u"Mirror":
            check_mirror_channel.delay(
                container=self, Mirror=Mirror)
            check_mirror_site.delay(
                container=self, Mirror=Mirror)

    def get_absolute_url(self):
        if self.channel.homepage:
            return u"/{0}.html".format(self.slug)
        long_slug = self.channel_long_slug or self.channel.long_slug
        return u"/{0}/{1}.html".format(long_slug, self.slug)

    @classmethod
    def get_children_models(cls):
        children = models.get_models()
        return [model for model in children
                if (model is not None and
                    issubclass(model, cls) and
                    model is not cls)]

    def get_thumb(self):
        return self.main_image

    @property
    def search_category(self):
        """for use in search result"""
        return _(self.child_class)

    def get_http_absolute_url(self):
        return u"http://{0}{1}".format(self.site_domain or self.site.domain,
                                       self.get_absolute_url())
    get_http_absolute_url.short_description = _(u'Get HTTP Absolute URL')

    def recommendation(self, child_class=False, query_slice=[None, 10]):

        if not child_class:
            child_class = self.child_class

        now = timezone.now()
        start = now - timezone.timedelta(
            days=settings.OPPS_RECOMMENDATION_RANGE_DAYS
        )

        cachekey = _cache_key(
            u'{0}-recommendation'.format(self.__class__.__name__),
            self.__class__, self.site_domain,
            u"{0}-{1}-{2}".format(child_class, self.channel_long_slug,
                                  self.slug))
        getcache = cache.get(cachekey)
        if getcache:
            return getcache

        containers = Container.objects.filter(
            site_domain=self.site_domain,
            child_class=child_class,
            channel_long_slug=self.channel_long_slug,
            date_available__range=(start, now),
            published=True
        ).exclude(pk=self.pk)

        tag_list = []
        if self.tags:
            tag_list = [t for t in self.tags.split(',')[:3]]
            containers = containers.filter(
                reduce(operator.or_, (Q(tags__contains=tag) for tag in
                                      tag_list)),
            )
        containers = containers.distinct().order_by(
            '-date_available')[slice(*query_slice)]

        _list = [a for a in containers]

        cache.set(cachekey, _list, 3600)
        return _list

    def inbox(self, containerbox=None):
        obj = ContainerBoxContainers.objects
        if containerbox:
            return obj.get(container=self.id,
                           containerbox__slug=containerbox)
        return obj.filter(container=self.id)

    def custom_fields(self):
        if not self.json:
            return {}
        return json.loads(self.json)


class ContainerImage(models.Model):
    container = models.ForeignKey(
        'containers.Container',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Container'),
    )
    order = models.PositiveIntegerField(_(u'Order'), default=0)
    image = models.ForeignKey(
        'images.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Image'),
    )

    caption = models.CharField(
        _(u"Caption"),
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _(u'Container image')
        verbose_name_plural = _(u'Container images')
        ordering = ('order',)

    def __unicode__(self):
        if self.image:
            return u"{0}".format(self.image.title)
        return u'Id:{0} - Order:{1}'.format(self.id, self.order)


class ContainerBox(BaseBox):

    title = models.CharField(
        _(u"Title"),
        null=True,
        blank=True,
        max_length=140,
    )
    title_url = models.CharField(
        _(u"Title Link"),
        null=True,
        blank=True,
        max_length=250,
    )
    main_image = models.ForeignKey(
        'images.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Main Image'),
    )
    main_image_caption = models.CharField(
        _(u"Main Image Caption"),
        max_length=4000,
        blank=True,
        null=True,
        help_text=_(u'Maximum characters 4000'),
    )
    containers = models.ManyToManyField(
        'containers.Container',
        null=True, blank=True,
        verbose_name=_(u'Container'),
        related_name='containerbox_containers',
        through='containers.ContainerBoxContainers'
    )
    queryset = models.ForeignKey(
        'boxes.QuerySet',
        null=True, blank=True,
        related_name='containerbox_querysets',
        verbose_name=_(u'Query Set')
    )

    content_group = models.CharField(
        _(u"Content Group"),
        max_length=255,
        default='default',
        help_text=_(u"Boxes in the same group do not allow repetitions")
    )

    class Meta:
        verbose_name = _(u'Container box')
        verbose_name_plural = _(u'Containers boxes')

    def __init__(self, *args, **kwargs):
        """
        to avoid re-execution of methods
        its results are cached in a local storage
        per instance cache
        """
        super(ContainerBox, self).__init__(*args, **kwargs)
        if not hasattr(self, 'local_cache'):
            self.local_cache = {}

    @property
    def has_content(self):
        # TODO: should check start/end available_dates
        if self.containerboxcontainers_set.exists():
            return True
        qs = self.get_queryset(use_local_cache=False)
        if qs and qs.exists():
            return True

    def ordered_containers(self, field='order', exclude_ids=None):
        cached = self.local_cache.get('ordered_containers', None)
        if cached:
            return cached

        exclude_ids = exclude_ids or []

        now = timezone.now()
        fallback = getattr(settings, 'OPPS_MULTISITE_FALLBACK', False)
        if not fallback:
            qs = self.containers.filter(
                models.Q(containerboxcontainers__date_end__gte=now) |
                models.Q(containerboxcontainers__date_end__isnull=True),
                published=True,
                date_available__lte=now,
                containerboxcontainers__date_available__lte=now
            ).exclude(
                id__in=exclude_ids
            ).order_by('containerboxcontainers__order').distinct()
        else:

            site_master = cache.get("site_master")

            if not site_master:
                site_master = Site.objects.order_by('id')[0]
                cache.set('site_master', site_master, 3600)

            boxes = [self]

            if fallback and site_master.pk != self.site_id:
                try:
                    master_box = self.__class__.objects.get(
                        site=site_master, slug=self.slug
                    )
                    boxes.insert(0, master_box)
                except self.__class__.DoesNotExist:
                    pass

            qs = ContainerBoxContainers.objects.filter(
                models.Q(date_end__gte=now) |
                models.Q(date_end__isnull=True),
                models.Q(container__published=True,
                         container__date_available__lte=now) |
                models.Q(container__isnull=True),
                containerbox__in=boxes,
                date_available__lte=now,
            ).exclude(
                container__id__in=exclude_ids
            ).order_by('-containerbox__site__id', 'order').distinct()

        self.local_cache['ordered_containers'] = qs
        return qs

    def ordered_box_containers(self, exclude_ids=None):

        fallback = getattr(settings, 'OPPS_MULTISITE_FALLBACK', False)
        if fallback:
            return self.ordered_containers(exclude_ids=exclude_ids)

        cached = self.local_cache.get('ordered_box_containers')
        if cached:
            return cached

        exclude_ids = exclude_ids or []

        now = timezone.now()
        qs = self.containerboxcontainers_set.prefetch_related(
            'main_image', 'container', 'container__main_image',
            'container__channel')
        qs = qs.filter(
            models.Q(date_end__gte=now) |
            models.Q(date_end__isnull=True),
            date_available__lte=now
        ).exclude(
            container_id__in=exclude_ids
        ).order_by('order').distinct()

        self.local_cache['ordered_box_containers'] = qs
        return qs

    def get_containers_queryset(self):
        if self.queryset:
            return self.queryset.get_queryset()
        else:
            return self.ordered_containers()

    def get_queryset(self, exclude_ids=None, use_local_cache=True):
        cached = self.local_cache.get('get_queryset')
        if use_local_cache and cached:
            return cached

        queryset = self.queryset and self.queryset.get_queryset(
            content_group=self.content_group,
            exclude_ids=exclude_ids,
            use_local_cache=use_local_cache
        )
        if use_local_cache:
            self.local_cache['get_queryset'] = queryset
        return queryset

    def clean(self):
        repeated = ContainerBox.objects.filter(
            site=self.site,
            slug=self.slug,
            channel_long_slug=self.channel.long_slug
        ).exclude(pk=self.pk)

        if repeated.exists():
            raise ValidationError(
                _(u"Already exists a ContainerBox with same slug and site")
            )


class ContainerBoxContainers(models.Model):
    URL_TARGET_CHOICES = (
        ('_blank', _(u'Load in a new window')),
        ('_self', _(u'Load in the same frame as it was clicked')),
        ('_parent', _(u'Load in the parent frameset')),
        ('_top', _(u'Load in the full body of the window'))
    )

    containerbox = models.ForeignKey(
        'containers.ContainerBox',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Container Box'),
    )
    container = models.ForeignKey(
        'containers.Container',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Container'),
    )

    order = models.PositiveIntegerField(_(u'Order'), default=0)
    aggregate = models.BooleanField(_(u'Aggregate container'), default=False)
    highlight = models.BooleanField(_(u'Highlight container'), default=False)
    date_available = models.DateTimeField(_(u"Date available"),
                                          default=timezone.now, null=True)
    date_end = models.DateTimeField(_(u"End date"), null=True, blank=True)

    title = models.CharField(_(u"Title"), max_length=140,
                             null=True, blank=True)

    hat = models.CharField(
        _(u"Hat"),
        max_length=140,
        null=True, blank=True,
    )

    main_image = models.ForeignKey(
        'images.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Main Image'),
    )
    main_image_caption = models.CharField(
        _(u"Main Image Caption"),
        max_length=4000,
        blank=True,
        null=True,
        help_text=_(u'Maximum characters 4000'),
    )

    url = models.CharField(_(u"URL"), max_length=255, null=True, blank=True)
    url_target = models.CharField(_(u"URL Target"), max_length=255,
                                  choices=URL_TARGET_CHOICES, default="_self",
                                  null=True, blank=True)

    class Meta:
        ordering = ('order',)
        verbose_name = _(u'Article box articles')
        verbose_name_plural = _(u'Article boxes articles')
        ordering = ('order', 'aggregate',)

    def __unicode__(self):
        if self.container:
            return u"{0}-{1}".format(self.containerbox.slug,
                                     self.container.slug)
        else:
            return u"{0}".format(self.containerbox.slug)

    def clean(self):
        if not self.container and not self.url:
            raise ValidationError(_(u'Please select a Container or insert a '
                                    u'URL!'))

        if self.container and not self.container.published:
            raise ValidationError(_(u'Article not published!'))


class ContainerRelated(models.Model):
    container = models.ForeignKey(
        'containers.Container',
        verbose_name=_(u'Container'),
        related_name='containerrelated_container'
    )

    related = models.ForeignKey(
        'containers.Container',
        verbose_name=_(u'Related Container'),
        related_name="%(app_label)s_%(class)s_container"
    )

    order = models.PositiveIntegerField(_(u'Order'), default=0)

    class Meta:
        verbose_name = _('Related content')
        verbose_name_plural = _('Related contents')
        ordering = ('order',)

    def __unicode__(self):
        return u"{0}->{1}".format(self.related.slug, self.container.slug)


class Mirror(Container):
    container = models.ForeignKey('containers.Container',
                                  related_name='containers_mirror',
                                  verbose_name=_(u'Container'))

    class Meta:
        verbose_name = _(u'Mirror')
        verbose_name_plural = _(u'Mirrors')

models.signals.post_delete.connect(delete_container, sender=Container)
