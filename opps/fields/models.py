#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.boxes.models import OPPS_APPS


FIELD_TYPE = (
    ('checkbox', _('CheckBox')),
    ('radio', _('Radio')),
    ('text', _('Text')),
    ('textarea', _('TextArea')),
)


class Field(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=255)
    application = models.CharField(_('Application'),
                                   max_length=255,
                                   choices=OPPS_APPS,
                                   db_index=True)
    type = models.CharField(_("Type"), max_length=15,
                            choices=FIELD_TYPE,
                            db_index=True)

    def __unicode__(self):
        return u"{} - {}".format(self.application, self.name)
