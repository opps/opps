# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable, BaseConfig
from opps.articles.signals import shorturl_generate


class FlatPage(Publishable):
    title = models.CharField(_(u"Title"), max_length=140, db_index=True)
    headline = models.TextField(_(u"Headline"), blank=True, null=True)
    slug = models.SlugField(
        _(u"URL"),
        db_index=True,
        max_length=150,
        unique=True,
    )
    short_url = models.URLField(
        _("Short URL"),
        null=True, blank=False,
    )
    show_in_menu = models.BooleanField(_(u"Show in menu?"), default=False)
    main_image = models.ForeignKey(
        'images.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Main Image'),
    )
    content = models.TextField(_(u"Content"))
    order = models.IntegerField(_(u"Order"), default=0)

    class META:
        verbose_name = _('Flat page')
        verbose_name_plural = _('Flat pages')

    def get_absolute_url(self):
        return "/page/{0}".format(self.slug)

    def get_http_absolute_url(self):
        return "http://{0}{1}".format(self.site.domain,
                                      self.get_absolute_url())
    get_http_absolute_url.short_description = 'URL'

    def __unicode__(self):
        return u"{0} - {1}".format(self.site.name, self.slug)


class FlatPageConfig(BaseConfig):
    """
    Default implementation
    """
    pass


models.signals.post_save.connect(shorturl_generate, sender=FlatPage)
