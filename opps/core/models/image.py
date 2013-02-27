# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from opps.core.models.published import Published
from opps.core.models.date import Date



class Image(Published, Date):

    image = models.ImageField(upload_to="opps_images/")
    description = models.CharField(_(u"Description"), max_length=255,
            null=True, blank=True)
