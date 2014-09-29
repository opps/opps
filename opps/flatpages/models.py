# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.containers.signals import shorturl_generate
from opps.articles.models import Article


class FlatPage(Article):
    show_in_menu = models.BooleanField(_(u"Show in menu?"), default=False)
    global_page = models.BooleanField(_(u"Show in all sites?"), default=False)
    content = models.TextField(_(u"Content"))
    order = models.IntegerField(_(u"Order"), default=0)

    class Meta:
        verbose_name = _(u'Flatpage')
        verbose_name_plural = _(u'Flatpages')

    def get_absolute_url(self):
        return u"/page/{0}".format(self.slug)

    def get_http_absolute_url(self):
        return u"http://{0}{1}".format(self.site.domain,
                                       self.get_absolute_url())
    get_http_absolute_url.short_description = 'URL'


models.signals.post_save.connect(shorturl_generate, sender=FlatPage)
