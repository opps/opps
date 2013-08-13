# -*- coding: utf-8 -*-
from urlparse import urlparse

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.cache import cache

from taggit.managers import TaggableManager

from .signals import redirect_generate, shorturl_generate, delete_article
from opps.core.models import Publishable, BaseBox, BaseConfig
from opps.core.models import Slugged
from opps.core.cache import _cache_key


class Article(Publishable, Slugged):
    title = models.CharField(_(u"Title"), max_length=140, db_index=True)
    headline = models.TextField(_(u"Headline"), blank=True)
    short_title = models.CharField(
        _(u"Short title"),
        max_length=140,
        null=True, blank=True,
    )
    hat = models.CharField(
        _(u"Hat"),
        max_length=140,
        null=True, blank=True,
    )
    short_url = models.URLField(
        _("Short URL"),
        null=True, blank=True,
    )
    site_iid = models.PositiveIntegerField(
        _(u"Site id"),
        max_length=4,
        null=True, blank=True,
        db_index=True,
    )
    site_domain = models.CharField(
        _(u"Site domain"),
        max_length=100,
        null=True, blank=True,
        db_index=True,
    )
    channel = models.ForeignKey(
        'channels.Channel',
        verbose_name=_(u"Channel"),
    )
    channel_name = models.CharField(
        _(u"Channel name"),
        max_length=140,
        null=True, blank=True,
        db_index=True,
    )
    channel_long_slug = models.CharField(
        _(u"Channel long slug"),
        max_length=250,
        null=True, blank=True,
        db_index=True,
    )
    child_class = models.CharField(
        _(u'Child class'),
        max_length=30,
        null=True, blank=True,
        db_index=True
    )
    child_app_label = models.CharField(
        _(u'Child app label'),
        max_length=30,
        null=True, blank=True,
        db_index=True
    )
    main_image = models.ForeignKey(
        'images.Image',
        null=True, blank=False,
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
    images = models.ManyToManyField(
        'images.Image',
        null=True, blank=True,
        related_name='article_images',
        through='articles.ArticleImage',
        verbose_name=_(u'Images')
    )
    sources = models.ManyToManyField(
        'sources.Source',
        null=True, blank=True,
        through='articles.ArticleSource',
        verbose_name=_(u'Sources')
    )
    tags = TaggableManager(blank=True, verbose_name=u'Tags')
    show_on_root_channel = models.BooleanField(
        _(u"Show on root channel?"),
        default=True
    )

    def __unicode__(self):
        return u"{}".format(self.get_absolute_url())

    class Meta:
        ordering = ['-date_available', 'title', 'channel_long_slug']
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        unique_together = ["site", "child_class", "channel_long_slug", "slug"]

    def save(self, *args, **kwargs):
        self.site_domain = self.site.domain
        self.site_iid = self.site.id
        self.channel_name = self.channel.name
        self.channel_long_slug = self.channel.long_slug
        self.child_class = self.__class__.__name__
        self.child_app_label = self._meta.app_label

        models.signals.post_save.connect(shorturl_generate,
                                         sender=self.__class__)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        TODO: get_absolute_url from child_app_label/child_class
        """
        if self.child_class != "Post":
            return "/{}/{}/{}".format(self.child_class.lower(),
                                      self.channel_long_slug, self.slug)
        return "/{}/{}".format(self.channel_long_slug, self.slug)

    def get_thumb(self):
        return self.main_image

    @property
    def search_category(self):
        """for use in search result"""
        return _(self.child_class)

    def get_http_absolute_url(self):
        return "http://{}{}".format(self.site_domain, self.get_absolute_url())

    get_http_absolute_url.short_description = 'URL'

    def recommendation(self):
        now = timezone.now()
        start = now - timezone.timedelta(
            days=settings.OPPS_RECOMMENDATION_RANGE_DAYS
        )

        cachekey = _cache_key(
            '{}-recommendation'.format(self.__class__.__name__),
            self.__class__, self.site_domain,
            u"{}-{}".format(self.channel_long_slug, self.slug))
        getcache = cache.get(cachekey)
        if getcache:
            return getcache

        tag_list = [t for t in self.tags.all()]
        _list = [a for a in Article.objects.filter(
            site_domain=self.site_domain,
            child_class=self.child_class,
            channel_long_slug=self.channel_long_slug,
            date_available__range=(start, now),
            published=True,
            tags__in=tag_list
        ).exclude(pk=self.pk).distinct().order_by('-date_available')[:10]]

        cache.set(cachekey, _list, 3600)
        return _list

    def all_images(self):
        cachekey = _cache_key(
            '{}-all_images'.format(self.__class__.__name__),
            self.__class__, self.site_domain,
            u"{}-{}".format(self.channel_long_slug, self.slug))
        getcache = cache.get(cachekey)
        if getcache:
            return getcache

        self.main_image.description = self.main_image_caption

        imgs = [self.main_image]
        images = self.images.prefetch_related('source').filter(
            published=True, date_available__lte=timezone.now()
        ).order_by('articleimage__order')

        if self.main_image:
            images = images.exclude(pk=self.main_image.pk)
        imgs += [i for i in images.distinct()]

        captions = {
            ai.image_id: ai.caption for ai in self.articleimage_articles.all()
        }
        for im in imgs:
            caption = captions.get(im.pk)
            if caption:
                im.description = caption

        cache.set(cachekey, imgs)
        return imgs


class Post(Article):
    content = models.TextField(_(u"Content"))
    albums = models.ManyToManyField(
        'articles.Album',
        null=True, blank=True,
        related_name='post_albums',
        verbose_name=_(u"Albums")
    )
    related_posts = models.ManyToManyField(
        'articles.Article',
        null=True, blank=True,
        related_name='post_relatedposts',
        through='articles.PostRelated',
        verbose_name=_(u'Related Posts'),
    )

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def all_images(self):
        cachekey = _cache_key(
            '{}main-all_images'.format(self.__class__.__name__),
            self.__class__, self.site_domain,
            u"{}-{}".format(self.channel_long_slug, self.slug))
        getcache = cache.get(cachekey)
        if getcache:
            return getcache

        imgs = super(Post, self).all_images()

        albums = self.albums.filter(
            published=True,
            date_available__lte=timezone.now()
        )
        for album in albums:
            images = album.images.prefetch_related('source').filter(
                published=True,
                date_available__lte=timezone.now()
            ).exclude(
                pk__in=[i.pk for i in imgs]
            )
            captions = {
                ai.image_id: ai.caption for ai in ArticleImage.objects.filter(
                    article_id=album.pk
                )
            }
            for image in images:
                caption = captions.get(image.pk)
                if caption:
                    image.description = caption

                imgs.append(image)

        cache.set(cachekey, imgs)
        return imgs

    def ordered_related(self, field='order'):
        """
        used in template
        """
        return self.related_posts.filter(
            published=True,
            date_available__lte=timezone.now()
        ).order_by(
            'postrelated_related__order'
        ).distinct()


class PostRelated(models.Model):
    post = models.ForeignKey(
        'articles.Post',
        verbose_name=_(u'Post'),
        null=True,
        blank=True,
        related_name='postrelated_post',
        on_delete=models.SET_NULL
    )
    related = models.ForeignKey(
        'articles.Article',
        verbose_name=_(u'Related Post'),
        null=True,
        blank=True,
        related_name='postrelated_related',
        on_delete=models.SET_NULL
    )
    order = models.PositiveIntegerField(_(u'Order'), default=0)

    class Meta:
        verbose_name = _('Related Post')
        verbose_name_plural = _('Related Posts')
        ordering = ('order',)

    def __unicode__(self):
        return u"{0}->{1}".format(self.related.slug, self.post.slug)


class AlbumRelated(models.Model):
    album = models.ForeignKey(
        'articles.Album',
        verbose_name=_(u'Album'),
        null=True,
        blank=True,
        related_name='albumrelated_album',
        on_delete=models.SET_NULL
    )
    related = models.ForeignKey(
        'articles.Article',
        verbose_name=_(u'Related Article'),
        null=True,
        blank=True,
        related_name='albumrelated_related',
        on_delete=models.SET_NULL
    )
    order = models.PositiveIntegerField(_(u'Order'), default=0)

    class Meta:
        verbose_name = _('Related Articles')
        verbose_name_plural = _('Related Articles')
        ordering = ('order',)

    def __unicode__(self):
        return u"{0}->{1}".format(self.related.slug, self.album.slug)


class Album(Article):
    related_articles = models.ManyToManyField(
        'articles.Article',
        null=True, blank=True,
        related_name='album_relatedposts',
        through='articles.AlbumRelated',
        verbose_name=_(u'Related Posts'),
    )

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')

    def get_absolute_url(self):
        return "/album/{}/{}".format(self.channel_long_slug, self.slug)

    def ordered_related(self, field='order'):
        """
        used in template
        """
        return self.related_articles.filter(
            published=True,
            date_available__lte=timezone.now()
        ).order_by(
            'albumrelated_related__order'
        ).distinct()


class Link(Article):
    url = models.URLField(_(u"URL"), null=True, blank=True)
    articles = models.ForeignKey(
        'articles.Article',
        null=True, blank=True,
        related_name='link_article',
        verbose_name=_(u'Articles')
    )

    class Meta:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def get_absolute_url(self):
        return "/link/{}/{}".format(
            self.channel_long_slug,
            self.slug
        )

    def is_local(self):
        try:
            url = urlparse(self.url)
            return url.netloc.replace('www', '') == self.site_domain
        except:
            return False

    def is_subdomain(self):
        return self.site_domain in self.url

    def clean(self):
        if not self.url and not self.articles:
            raise ValidationError(_('URL field is required.'))

        self.url = self.url
        if self.articles:
            self.url = self.articles.get_absolute_url()


class ArticleSource(models.Model):
    article = models.ForeignKey(
        'articles.Article',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='articlesource_articles',
        verbose_name=_(u'Article'),
    )
    source = models.ForeignKey(
        'sources.Source',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='articlesource_sources',
        verbose_name=_(u'Source'),
    )
    order = models.PositiveIntegerField(_(u'Order'), default=0)

    class Meta:
        verbose_name = _('Article source')
        verbose_name_plural = _('Article sources')
        ordering = ('order',)

    def __unicode__(self):
        return u"{}".format(self.source.slug)


class ArticleImage(models.Model):
    article = models.ForeignKey(
        'articles.Article',
        verbose_name=_(u'Article'),
        null=True, blank=True,
        related_name='articleimage_articles',
        on_delete=models.SET_NULL
    )
    image = models.ForeignKey(
        'images.Image',
        verbose_name=_(u'Image'),
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    order = models.PositiveIntegerField(_(u'Order'), default=0)
    caption = models.CharField(
        _(u"Caption"),
        max_length=4000,
        blank=True,
        null=True,
        help_text=_(u'Maximum characters 4000')
    )

    class Meta:
        verbose_name = _(u'Article image')
        verbose_name_plural = _(u'Article images')
        ordering = ('order',)

    def __unicode__(self):
        return u"{}".format(self.image.title)


class ArticleBox(BaseBox):

    title = models.CharField(
        _(u"Title"),
        null=True,
        blank=True,
        max_length=140,
    )
    articles = models.ManyToManyField(
        'articles.Article',
        null=True, blank=True,
        related_name='articlebox_articles',
        through='articles.ArticleBoxArticles',
        verbose_name=_(u'Articles')
    )
    queryset = models.ForeignKey(
        'boxes.QuerySet',
        null=True, blank=True,
        related_name='articlebox_querysets',
        verbose_name=_(u'Query Set')
    )

    class Meta:
        verbose_name = _('Article box')
        verbose_name_plural = _('Articles boxes')

    def ordered_articles(self, field='order'):
        now = timezone.now()
        qs = self.articles.filter(
            models.Q(articleboxarticles_articles__date_end__gte=now) |
            models.Q(articleboxarticles_articles__date_end__isnull=True),
            published=True,
            date_available__lte=now,
            articleboxarticles_articles__date_available__lte=now
        ).order_by('articleboxarticles_articles__order').distinct()
        return qs

    def get_queryset(self):
        """
        for backwards compatibility
        """
        return self.queryset.get_queryset()


class ArticleBoxArticles(models.Model):
    articlebox = models.ForeignKey(
        'articles.ArticleBox',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='articleboxarticles_articleboxes',
        verbose_name=_(u'Article Box'),
    )
    article = models.ForeignKey(
        'articles.Article',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='articleboxarticles_articles',
        verbose_name=_(u'Article'),
    )
    order = models.PositiveIntegerField(_(u'Order'), default=0)
    date_available = models.DateTimeField(_(u"Date available"),
                                          default=timezone.now, null=True)
    date_end = models.DateTimeField(_(u"End date"), null=True, blank=True)

    class Meta:
        ordering = ('order',)
        verbose_name = _('Article box articles')
        verbose_name_plural = _('Article boxes articles')

    def __unicode__(self):
        return u"{0}-{1}".format(self.articlebox.slug, self.article.slug)

    def clean(self):

        if not self.article.published:
            raise ValidationError(_(u'Article not published!'))


class ArticleConfig(BaseConfig):
    """
    Default implementation
    """

    class Meta:
        verbose_name = _('Article config')
        verbose_name_plural = _('Article configs')
        permissions = (("developer", "Developer"),)
        unique_together = ("key_group", "key", "site", "channel", "article")


models.signals.post_save.connect(redirect_generate, sender=Link)
models.signals.post_delete.connect(delete_article, sender=Article)
