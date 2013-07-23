# -*- coding: utf-8 -*-
from django.db.models.fields import CharField


class TagField(CharField):
    def to_python(self, value):
        return value
