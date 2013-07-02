#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.archives.models import Archive


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

    fit_in = models.BooleanField(_(u'Fit in'), default=True,
                                 help_text=_(u'flag that indicates that '
                                             u'thumbor should fit the image '
                                             u'in the box defined by width x '
                                             u'height'))

    smart = models.BooleanField(_(u'Smart'), default=False,
                                help_text=_(u'Flag that indicates that'
                                            u'thumbor should use smart '
                                            u'cropping;'))

    class Meta:
        abstract = True

    def clean(self):
        self.crop_x1 = len(self.crop_x1) == 0 if self.crop_x1 else 0
        self.crop_x2 = len(self.crop_x2) == 0 if self.crop_x2 else 0
        self.crop_y1 = len(self.crop_y1) == 0 if self.crop_y1 else 0
        self.crop_y2 = len(self.crop_y2) == 0 if self.crop_y2 else 0

        super(Cropping, self).clean()

    def save(self, *args, **kwargs):
        self.crop_example = self.archive.url
        super(Cropping, self).save(*args, **kwargs)


class Image(Archive, Cropping):

    class META:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
