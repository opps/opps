# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.redirects.models import Redirect

from taggit.managers import TaggableManager
from googl.short import GooglUrlShort

from opps.core.models import Publishable, BaseBox, BaseConfig
from opps.core.models import Slugged


class Article(Publishable, Slugged):
    title = models.CharField(_(u"Title"), max_length=140, db_index=True)
    headline = models.TextField(_(u"Headline"), blank=True)
    short_title = models.CharField(
        _(u"Short title"),
        max_length=140,
        null=True, blank=False,
    )
    hat = models.CharField(
        _(u"Hat"),
        max_length=140,
        null=True, blank=True,
    )
    short_url = models.URLField(
        _("Short URL"),
        null=True, blank=False,
    )
    channel = models.ForeignKey(
        'channels.Channel',
        verbose_name=_(u"Channel"),
    )
    channel_name = models.CharField(
        _(u"Channel name"),
        max_length=140,
        null=True, blank=False,
        db_index=True,
    )
    channel_long_slug = models.CharField(
        _(u"Channel long slug"),
        max_length=250,
        null=True, blank=False,
        db_index=True,
    )
    child_class = models.CharField(
        _(u'Child class'),
        max_length=30,
        null=True, blank=False,
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
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return u"{}".format(self.get_absolute_url())

    class Meta:
        ordering = ['-date_available', 'title', 'channel_long_slug']

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = GooglUrlShort(self.get_http_absolute_url())\
                .short()
        self.channel_name = self.channel.name
        self.channel_long_slug = self.channel.long_slug
        self.child_class = self.__class__.__name__
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/{}/{}".format(self.channel_long_slug, self.slug)

    def get_thumb(self):
        return self.main_image

    @property
    def search_category(self):
        """for use in search result"""
        return _(self.child_class)

    def get_http_absolute_url(self):
        return "http://{}{}".format(self.site.domain,
                                    self.get_absolute_url())
    get_http_absolute_url.short_description = 'URL'

    def recommendation(self):
        tag_list = [t for t in self.tags.all()[:3]]
        return [a for a in Article.objects.filter(
            child_class=self.child_class,
            date_available__lte=timezone.now(),
            published=True,
            tags__in=tag_list).exclude(
                pk=self.pk).distinct().order_by('pk')[:10]]

    def all_images(self):
        imgs = [i for i in self.images.filter(
            published=True, date_available__lte=timezone.now())]

        return list(set(imgs))


class Post(Article):
    content = models.TextField(_(u"Content"))
    albums = models.ManyToManyField(
        'articles.Album',
        null=True, blank=True,
        related_name='post_albums',
    )
    related_posts = models.ManyToManyField(
        'articles.Post',
        null=True, blank=True,
        related_name='post_relatedposts',
        through='articles.PostRelated',
    )

    def all_images(self):
        imgs = super(Post, self).all_images()

        imgs += [i for a in self.albums.filter(
            published=True, date_available__lte=timezone.now())
            for i in a.images.filter(published=True,
                                     date_available__lte=timezone.now())]
        return list(set(imgs))


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

    def __unicode__(self):
        return u"{0}->{1}".format(self.related.slug, self.post.slug)


class Album(Article):
    def get_absolute_url(self):
        return "/album/{}/{}".format(self.channel_long_slug, self.slug)

    def get_http_absolute_url(self):
        return "http://{}{}".format(self.site.domain, self.get_absolute_url())


class Link(Article):
    url = models.URLField(_(u"URL"), null=True, blank=True)
    articles = models.ForeignKey(
        'articles.Article',
        null=True, blank=True,
        related_name='link_article'
    )

    def get_absolute_url(self):
        return "/link/{0}/{1}".format(self.channel.long_slug, self.slug)

    def get_http_absolute_url(self):
        protocol, path = "http://{0}/{1}".format(
            self.channel, self.slug).split(self.site.domain)
        return "{0}{1}/link{2}".format(protocol, self.site, path)

    def clean(self):
        if not self.url and not self.articles:
            raise ValidationError(_('URL field is required.'))

        if self.articles:
            self.url = self.articles.get_http_absolute_url()

    def save(self, *args, **kwargs):
        obj, create = Redirect.objects.get_or_create(
            old_path=self.get_absolute_url(), site=self.site)
        obj.new_path = self.url
        obj.save()
        super(Link, self).save(*args, **kwargs)


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

    def __unicode__(self):
        return u"{}".format(self.image.title)


class ArticleBox(BaseBox):

    articles = models.ManyToManyField(
        'articles.Article',
        null=True, blank=True,
        related_name='articlebox_articles',
        through='articles.ArticleBoxArticles'
    )
    queryset = models.ForeignKey(
        'boxes.QuerySet',
        null=True, blank=True,
        verbose_name=_(u'Query Set')
    )

    def get_queryset(self):
        _app, _model = self.queryset.model.split('.')
        model = models.get_model(_app, _model)

        queryset = model.objects.filter(published=True,
                                        date_available__lte=timezone.now())
        if self.queryset.channel:
            queryset = queryset.filter(channel=self.queryset.channel)
        queryset = queryset.order_by('{0}id'.format(self.queryset.order))[
            :self.queryset.limit]

        return queryset


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

    def __unicode__(self):
        return u"{0}-{1}".format(self.articlebox.slug, self.article.slug)

    def clean(self):

        if not self.article.published:
            raise ValidationError(_(u'Article not published!'))

        if self.article.date_available >= timezone.now():
            raise ValidationError(_(u'Article date available is greater than '
                                    u'today!'))


class ArticleConfig(BaseConfig):
    """
    Default implementation
    """
    pass
