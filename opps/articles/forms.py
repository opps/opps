#!/usr/bin/env python
# -*- coding: utf-8 -*-
from opps.core.widgets import OppsEditor
from opps.containers.forms import ContainerAdminForm

from .models import Post, Album, Link


class PostAdminForm(ContainerAdminForm):
    multiupload_link = '/fileupload/image/'

    class Meta:
        model = Post
        widgets = {'content': OppsEditor()}


class AlbumAdminForm(ContainerAdminForm):
    multiupload_link = '/fileupload/image/'

    class Meta:
        model = Album
        widgets = {
            'headline': OppsEditor()
        }


class LinkAdminForm(ContainerAdminForm):
    class Meta:
        model = Link
