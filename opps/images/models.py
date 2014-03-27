#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.archives.models import Archive
from opps.core.tags.models import Tagged
from .generate import image_url as url

HALIGN_CHOICES = (
    ('left', _('Left')),
    ('center', _('Center')),
    ('right', _('Right'))
)
VALIGN_CHOICES = (
    ('top', _('Top')),
    ('middle', _('Middle')),
    ('bottom', _('Bottom'))
)


class Cropping(models.Model):
    crop_example = models.CharField(_(u"Crop Example"), max_length=255,
                                    null=True, blank=True)
    crop_x1 = models.PositiveSmallIntegerField(default=0, null=True,
                                               blank=True)
    crop_x2 = models.PositiveSmallIntegerField(default=0, null=True,
                                               blank=True)
    crop_y1 = models.PositiveSmallIntegerField(default=0, null=True,
                                               blank=True)
    crop_y2 = models.PositiveSmallIntegerField(default=0, null=True,
                                               blank=True)
    flip = models.BooleanField(_(u'Flip'), default=False,
                               help_text=_(u'Flag that indicates that '
                                           u'thumbor should flip '
                                           u'horizontally (on the vertical '
                                           u'axis) the image'))
    flop = models.BooleanField(_(u'Flop'), default=False,
                               help_text=_(u'Flag that indicates that '
                                           u'thumbor should flip '
                                           u'vertically (on the horizontal '
                                           u'axis) the image'))
    halign = models.CharField(_(u'Horizontal Align'), default=False,
                              max_length=6,
                              null=True, blank=True,
                              choices=HALIGN_CHOICES,
                              help_text=_(u'Horizontal alignment that '
                                          u'thumbor should use for cropping'))
    valign = models.CharField(_(u'Vertical Align'), default=False,
                              max_length=6,
                              null=True, blank=True,
                              choices=VALIGN_CHOICES,
                              help_text=_(u'Vertical alignment that '
                                          u'thumbor should use for cropping'))

    fit_in = models.BooleanField(_(u'Fit in'), default=False,
                                 help_text=_(u'Flag that indicates that '
                                             u'thumbor should fit the image '
                                             u'in the box defined by width x '
                                             u'height'))

    smart = models.BooleanField(_(u'Smart'), default=False,
                                help_text=_(u'Flag that indicates that'
                                            u' thumbor should use smart '
                                            u'cropping'))

    class Meta:
        abstract = True

    def clean(self):
        super(Cropping, self).clean()

    def save(self, *args, **kwargs):
        if self.archive and settings.THUMBOR_ENABLED:
            self.crop_example = self.archive.url
        else:
            self.crop_example = self.image_url()

        super(Cropping, self).save(*args, **kwargs)


class Image(Archive, Cropping, Tagged):

    def clean(self):
        items = ['x1', 'x2', 'y1', 'y2']
        for item in items:
            prop = getattr(self, 'crop_' + item, None)
            if not prop or prop is None or prop in ['', ' ']:
                setattr(self, 'crop_' + item, 0)

        if self.archive and settings.THUMBOR_ENABLED:
            self.crop_example = self.archive.url
        else:
            self.crop_example = self.image_url()

        super(Image, self).clean()

    def image_url(self, *args, **kwargs):
        if self.archive:
            return url(self.archive.url, *args, **kwargs)
        elif self.archive_link:
            return self.archive_link
        return ''

    class Meta:
        verbose_name = _(u'Image')
        verbose_name_plural = _(u'Images')
