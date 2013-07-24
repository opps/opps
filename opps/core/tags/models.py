# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from opps.core.models import Date, Slugged


class Tag(Date, Slugged):
    name = models.CharField(_(u'Tag'), max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    __unicode__ = lambda self: self.name

    class Meta:
        verbose_name = _(u'Tag')
        verbose_name_plural = _(u'Tags')


class Tagged(models.Model):
    tags = models.CharField(_(u'Tags'), max_length=4000, blank=True,
                            help_text=_(u'A comma-separated list of tags.'))

    def save(self, *args, **kwargs):
        if self.tags:
            for tag in self.tags.split(','):
                Tag.objects.get_or_create(name=tag)

        super(Tagged, self).save(*args, **kwargs)

    def get_tags(self):
        if self.tags:
            return [Tag.objects.get(name=i) for i in self.tags.split(',')]

    class Meta:
        abstract = True
