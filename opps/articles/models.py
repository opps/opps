# -*- coding: utf-8 -*-
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
    images = models.ManyToManyField(
        'images.Image',
        null=True, blank=True,
        related_name='article_images',
        through='articles.ArticleImage',
    )
    sources = models.ManyToManyField(
        'sources.Source',
        null=True, blank=True,
        through='articles.ArticleSource',
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
        return "http://{}{}".format(self.site.domain, self.get_absolute_url())

    get_http_absolute_url.short_description = 'URL'

    def recommendation(self):
        cachekey = _cache_key(
            '{}-recommendation'.format(self.__class__.__name__),
            self.__class__, self.site, u"{}-{}".format(self.channel_long_slug,
                                                       self.slug))
        getcache = cache.get(cachekey)
        if getcache:
            return getcache

        tag_list = [t for t in self.tags.all()[:3]]
        _list = [a for a in Article.objects.filter(
            child_class=self.child_class,
            channel_long_slug=self.channel_long_slug,
            date_available__lte=timezone.now(),
            published=True,
            tags__in=tag_list).exclude(
                pk=self.pk).distinct().all().order_by('pk')[:10]]

        cache.set(cachekey, _list)
        return _list

    def all_images(self):
        cachekey = _cache_key(
            '{}-all_images'.format(self.__class__.__name__),
            self.__class__, self.site, u"{}-{}".format(self.channel_long_slug,
                                                       self.slug))
        getcache = cache.get(cachekey)
        if getcache:
            return getcache

        imgs = [self.main_image]
        images = self.images.filter(
            published=True, date_available__lte=timezone.now()
        ).order_by('articleimage__order', '-date_available')

        if self.main_image:
            images = images.exclude(pk=self.main_image.pk)
        imgs += [i for i in images.distinct()]

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
        'articles.Post',
        null=True, blank=True,
        related_name='post_relatedposts',
        through='articles.PostRelated',
    )

    class META:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def all_images(self):
        cachekey = _cache_key(
            '{}main-all_images'.format(self.__class__.__name__),
            self.__class__, self.site, u"{}-{}".format(self.channel_long_slug,
                                                       self.slug))
        getcache = cache.get(cachekey)
        if getcache:
            return getcache

        imgs = super(Post, self).all_images()
        imgs += [
            i for a in self.albums.filter(
                published=True,
                date_available__lte=timezone.now()
            ).distinct()
            for i in a.images.filter(
                published=True,
                date_available__lte=timezone.now()
            ).exclude(pk__in=[i.pk for i in imgs]).distinct()
        ]

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
        'articles.Post',
        verbose_name=_(u'Related Post'),
        null=True,
        blank=True,
        related_name='postrelated_related',
        on_delete=models.SET_NULL
    )
    order = models.PositiveIntegerField(_(u'Order'), default=0)

    class META:
        verbose_name = _('Post related')
        verbose_name_plural = _('Post relateds')
        ordering = ('order',)

    def __unicode__(self):
        return u"{0}->{1}".format(self.related.slug, self.post.slug)


class Album(Article):
    class META:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')

    def get_absolute_url(self):
        return "/album/{}/{}".format(self.channel_long_slug, self.slug)


class Link(Article):
    url = models.URLField(_(u"URL"), null=True, blank=True)
    articles = models.ForeignKey(
        'articles.Article',
        null=True, blank=True,
        related_name='link_article'
    )

    class META:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def get_absolute_url(self):
        return "/link/{}/{}".format(
            self.channel_long_slug,
            self.slug
        )

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

    class META:
        verbose_name = _('Article source')
        verbose_name_plural = _('Article sources')

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

    class META:
        verbose_name = _('Article image')
        verbose_name_plural = _('Article images')

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
        through='articles.ArticleBoxArticles'
    )
    queryset = models.ForeignKey(
        'boxes.QuerySet',
        null=True, blank=True,
        related_name='articlebox_querysets',
        verbose_name=_(u'Query Set')
    )

    class META:
        verbose_name = _('Article box')
        verbose_name_plural = _('Articles boxes')

    def ordered_articles(self, field='order'):
        now = timezone.now()
        qs = self.articles.filter(
            published=True,
            date_available__lte=now,
            articleboxarticles_articles__date_available__lte=now
        ).filter(
            models.Q(articleboxarticles_articles__date_end__gte=now) |
            models.Q(articleboxarticles_articles__date_end__isnull=True)
        )
        return qs.order_by('articleboxarticles_articles__order').distinct()

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

    class META:
        verbose_name = _('Article config')
        verbose_name_plural = _('Article configs')


models.signals.post_save.connect(redirect_generate, sender=Link)
models.signals.post_delete.connect(delete_article, sender=Article)
