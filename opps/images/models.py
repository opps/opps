# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from opps.core.models.publisher import Publisher

from sorl.thumbnail import ImageField, get_thumbnail



CROP_TYPE = (("center", u"center"),)

class ImageCrop(models.Model):

    type = models.CharField(_(u"Type"), max_length=15, choices=CROP_TYPE)
    width = models.IntegerField()
    height = models.IntegerField()
    quality = models.IntegerField(validators=[MinValueValidator(20),
        MaxValueValidator(100)])

    def __unicode__(self):
        return "{0} x {1} ({2})".format(self.width, self.height, self.type)


class Image(Publisher):

    image = ImageField(upload_to="opps_images/")
    description = models.CharField(_(u"Description"), max_length=255,
            null=True, blank=True)
    crop = models.ManyToManyField(ImageCrop, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.crop:
            import pdb; pdb.set_trace()
            for x in self.crop.all():
                get_thumbnail(self.image,
                        "{0}x{1}".format(x.width, x.height),
                        crop=x.type, quality=x.quality)

        super(Image, self).save(*args, **kwargs)
