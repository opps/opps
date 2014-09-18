#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


FIELD_TYPE = (
    ('checkbox', _('Checkbox')),
    ('radio', _('Radio')),
    ('text', _('Text')),
    ('textarea', _('Textarea')),
)


class Field(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=255)
    application = models.CharField(_('Application'),
                                   max_length=255,
                                   db_index=True)
    type = models.CharField(_("Type"), max_length=15,
                            choices=FIELD_TYPE,
                            db_index=True)

    def __unicode__(self):
        return u"{0} - {1}".format(self.application, self.name)

    class Meta:
        verbose_name = _(u'Field')
        verbose_name_plural = _(u'Fields')


class Option(models.Model):
    field = models.ForeignKey('fields.Field')
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=140)
    value = models.CharField(_('Value'), max_length=255)

    def __unicode__(self):
        return u"{0} - {1}".format(self.field.slug, self.name)

    class Meta:
        verbose_name = _(u'Option')
        verbose_name_plural = _(u'Options')


class FieldOption(models.Model):
    field = models.ForeignKey('fields.Field')
    option = models.ForeignKey('fields.Option')
    order = models.PositiveIntegerField(_(u'Order'), default=0)

    def __unicode__(self):
        return u"{0} - {1}".format(self.field.slug, self.option.slug)

    class Meta:
        ordering = ['-order']
        verbose_name = _('Field option')
        verbose_name_plural = _('Field options')
