# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.db import models

from opps.images.models import Cropping, HALIGN_CHOICES, VALIGN_CHOICES


class CroppingFields(TestCase):
    def test_crop_example(self):
        field = Cropping._meta.get_field_by_name('crop_example')[0]
        self.assertTrue(field.__class__, models.CharField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_crop_x1(self):
        field = Cropping._meta.get_field_by_name('crop_x1')[0]
        self.assertTrue(field.__class__, models.PositiveSmallIntegerField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_crop_x2(self):
        field = Cropping._meta.get_field_by_name('crop_x2')[0]
        self.assertTrue(field.__class__, models.PositiveSmallIntegerField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_crop_y1(self):
        field = Cropping._meta.get_field_by_name('crop_y1')[0]
        self.assertTrue(field.__class__, models.PositiveSmallIntegerField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_crop_y2(self):
        field = Cropping._meta.get_field_by_name('crop_y2')[0]
        self.assertTrue(field.__class__, models.PositiveSmallIntegerField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_flip(self):
        field = Cropping._meta.get_field_by_name('flip')[0]
        self.assertTrue(field.__class__, models.BooleanField)
        self.assertFalse(field.default)

    def test_flop(self):
        field = Cropping._meta.get_field_by_name('flop')[0]
        self.assertTrue(field.__class__, models.BooleanField)
        self.assertFalse(field.default)

    def test_halign(self):
        field = Cropping._meta.get_field_by_name('halign')[0]
        self.assertTrue(field.__class__, models.CharField)
        self.assertFalse(field.default)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.choices, HALIGN_CHOICES)

    def test_valign(self):
        field = Cropping._meta.get_field_by_name('valign')[0]
        self.assertTrue(field.__class__, models.CharField)
        self.assertFalse(field.default)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.choices, VALIGN_CHOICES)

    def test_fit_in(self):
        field = Cropping._meta.get_field_by_name('fit_in')[0]
        self.assertTrue(field.__class__, models.BooleanField)
        self.assertFalse(field.default)

    def test_smart(self):
        field = Cropping._meta.get_field_by_name('smart')[0]
        self.assertTrue(field.__class__, models.BooleanField)
        self.assertFalse(field.default)
