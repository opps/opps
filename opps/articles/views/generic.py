#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django import template
from django.conf import settings

from opps.articles.models import ArticleBox, Article, Album
from opps.channels.models import Channel


class OppsView(object):

    context_object_name = "context"
    paginate_by = settings.OPPS_PAGINATE_BY
    limit = settings.OPPS_VIEWS_LIMIT

    def __init__(self):
        self.slug = None
        self.channel = None
        self.long_slug = None
        self.channel_long_slug = []
        self.article = None
        self.excluded_ids = set()

    def get_context_data(self, **kwargs):
        context = super(OppsView, self).get_context_data(**kwargs)

        # channel is needed everywhere
        self.channel = self.channel or Channel.objects.get_homepage(
            site=get_current_site(self.request)
        )

        if hasattr(self, 'articleboxes'):
            context['articleboxes'] = self.articleboxes
        else:
            context['articleboxes'] = ArticleBox.objects.filter(
                channel__long_slug=self.long_slug)
            for box in context['articleboxes']:
                self.excluded_ids.update(
                    [a.pk for a in box.ordered_articles()]
                )

        filters = {}
        filters['site_domain'] = self.site
        filters['channel_long_slug__in'] = self.channel_long_slug
        filters['date_available__lte'] = timezone.now()
        filters['published'] = True
        filters['show_on_root_channel'] = True
        article = Article.objects.filter(**filters)

        context['posts'] = article.filter(
            child_class='Post'
        ).exclude(pk__in=self.excluded_ids)[:self.limit]

        context['albums'] = Album.objects.filter(
            **filters
        ).exclude(pk__in=self.excluded_ids)[:self.limit]

        context['channel'] = {}
        context['channel']['long_slug'] = self.long_slug
        if self.channel:
            context['channel']['slug'] = self.channel.slug
            context['channel']['title'] = self.channel.title
            context['channel']['level'] = self.channel.get_level()
            context['channel']['root'] = self.channel.get_root()

        if self.slug:
            context['articleboxes'] = context['articleboxes'].filter(
                article__slug=self.slug)

        return context

    def get_template_folder(self):
        domain_folder = self.type
        if settings.SITE_ID > 1:
            domain_folder = "{0}/{1}".format(self.site, self.type)
        return domain_folder

    def get_long_slug(self):
        self.long_slug = self.kwargs.get('channel__long_slug', None)
        try:
            if not self.long_slug:
                self.long_slug = Channel.objects.get_homepage(
                    site=self.site).long_slug
        except AttributeError:
            pass
        return self.long_slug

    def set_channel_rules(self):
        self.channel = get_object_or_404(Channel, site__domain=self.site,
                                         long_slug=self.long_slug,
                                         date_available__lte=timezone.now(),
                                         published=True)
        self.long_slug = self.channel.long_slug

        self.channel_long_slug = [self.long_slug]
        for children in self.channel.get_children():
            self.channel_long_slug.append(children.long_slug)

    def check_template(self, _template):
        try:
            template.loader.get_template(_template)
            return True
        except template.TemplateDoesNotExist:
            return False


class OppsList(OppsView, ListView):

    def get_template_names(self):
        names = []
        domain_folder = self.get_template_folder()

        # look for a different template only if defined in settings
        # default should be OPPS_PAGINATE_SUFFIX = "_paginated"
        # if set OPPS_PAGINATE_NOT_APP = ['TagList'] not set paginate_suffix
        if self.request and self.request.GET.get('page') and\
           self.__class__.__name__ not in settings.OPPS_PAGINATE_NOT_APP:
            self.paginate_suffix = settings.OPPS_PAGINATE_SUFFIX
            self.template_name_suffix = "_list{}".format(self.paginate_suffix)
        else:
            self.paginate_suffix = ''

        if self.channel:
            if self.channel.group and self.channel.parent:

                _template = '{}/_{}{}.html'.format(
                    domain_folder,
                    self.channel.parent.long_slug,
                    self.paginate_suffix
                )
                names.append(_template)

                _template = '{}/_post_list{}.html'.format(
                    domain_folder,
                    # self.channel.parent.long_slug,
                    self.paginate_suffix
                )
                names.append(_template)

        names.append(
            '{}/{}{}.html'.format(
                domain_folder,
                self.long_slug,
                self.paginate_suffix
            )
        )

        try:
            names = names + super(OppsList, self).get_template_names()
        except ImproperlyConfigured:
            pass

        if self.paginate_suffix:
            # use the default _paginated.html if no template found
            names.append(
                "{}/{}.html".format(domain_folder, self.paginate_suffix)
            )

        return names

    @property
    def queryset(self):
        self.site = get_current_site(self.request).domain
        self.long_slug = self.get_long_slug()

        if not self.long_slug:
            return None

        self.set_channel_rules()

        self.articleboxes = ArticleBox.objects.filter(
            channel__long_slug=self.long_slug)

        for box in self.articleboxes:
            self.excluded_ids.update([a.pk for a in box.ordered_articles()])

        self.article = self.model.objects.filter(
            site_domain=self.site,
            channel_long_slug__in=self.channel_long_slug,
            date_available__lte=timezone.now(),
            published=True,
            show_on_root_channel=True
        ).exclude(pk__in=self.excluded_ids)

        if self.limit:
            self.article = self.article[:self.limit]

        return self.article._clone()


class OppsDetail(OppsView, DetailView):

    def get_template_names(self):
        names = []
        domain_folder = self.get_template_folder()

        names.append('{}/{}/{}.html'.format(
            domain_folder, self.long_slug, self.slug))
        names.append('{}/{}.html'.format(domain_folder, self.long_slug))

        try:
            names = names + super(OppsDetail, self).get_template_names()
        except ImproperlyConfigured:
            pass

        return names

    @property
    def queryset(self):
        self.site = get_current_site(self.request).domain
        self.slug = self.kwargs.get('slug')
        self.long_slug = self.get_long_slug()
        if not self.long_slug:
            return None

        self.set_channel_rules()

        filters = dict(
            site_domain=self.site,
            channel_long_slug=self.long_slug,
            slug=self.slug
        )

        preview_enabled = self.request.user and self.request.user.is_staff

        if not preview_enabled:
            filters['date_available__lte'] = timezone.now()
            filters['published'] = True

        self.article = self.model.objects.filter(
            **filters
        )

        self.excluded_ids.update([a.pk for a in self.article])

        return self.article._clone()
