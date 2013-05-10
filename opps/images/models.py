# -*- coding: utf-8 -*-
import uuid
import os
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from taggit.models import TaggedItemBase
from taggit.managers import TaggableManager

from opps.core.models import Publishable, Slugged


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


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{0}-{1}.{2}".format(uuid.uuid4(), instance.slug, ext)
    d = datetime.now()
    folder = "images/{0}".format(d.strftime("%Y/%m/%d/"))
    return os.path.join(folder, filename)


class TaggedImage(TaggedItemBase):
    """Tag for images """
    content_object = models.ForeignKey('images.Image')


class Cropping(models.Model):
    crop_example = models.CharField(_(u"Crop Example"), max_length=140,
                                    null=True, blank=True)
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

    def save(self, *args, **kwargs):
        self.crop_example = self.image.url
        super(Cropping, self).save(*args, **kwargs)


class Image(Publishable, Slugged, Cropping):

    title = models.CharField(_(u"Title"), max_length=140, db_index=True)
    image = models.ImageField(upload_to=get_file_path)
    description = models.TextField(_(u"Description"), null=True, blank=True)
    tags = TaggableManager(blank=True, through=TaggedImage,
                           verbose_name=u'Tags')

    source = models.ForeignKey('sources.Source', null=True, blank=True)

    class META:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        unique_together = ['site', 'slug']

    def __unicode__(self):
        return u"{}-{}".format(self.site, self.slug)

    def get_absolute_url(self):
        if self.date_available <= timezone.now() and self.published:
            return self.image.url
        return u""
