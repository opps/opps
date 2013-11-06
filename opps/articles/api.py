#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils import timezone

from tastypie.resources import ModelResource

from opps.api import MetaBase

from .models import Post as PostModel
from .models import Album as AlbumModel
from .models import Link as LinkModel


class Post(ModelResource):
    class Meta(MetaBase):
        queryset = PostModel.objects.filter(
            published=True,
            date_available__lte=timezone.now()
        )


class Album(ModelResource):
    class Meta(MetaBase):
        queryset = AlbumModel.objects.filter(
            published=True,
            date_available__lte=timezone.now()
        )


class Link(ModelResource):
    class Meta(MetaBase):
        queryset = LinkModel.objects.filter(
            published=True,
            date_available__lte=timezone.now()
        )
