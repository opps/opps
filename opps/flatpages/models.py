# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import BaseConfig
from opps.articles.signals import shorturl_generate
from opps.articles.models import Article


class FlatPage(Article):
    show_in_menu = models.BooleanField(_(u"Show in menu?"), default=False)
    content = models.TextField(_(u"Content"))
    order = models.IntegerField(_(u"Order"), default=0)

    class META:
        verbose_name = _(u'Flat page')
        verbose_name_plural = _(u'Flat pages')

    def get_absolute_url(self):
        return u"/page/{0}".format(self.slug)

    def get_http_absolute_url(self):
        return u"http://{0}{1}".format(self.site.domain,
                                       self.get_absolute_url())
    get_http_absolute_url.short_description = 'URL'


class FlatPageConfig(BaseConfig):
    """
    Default implementation
    """
    pass


models.signals.post_save.connect(shorturl_generate, sender=FlatPage)
