#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tastypie.constants import ALL
from tastypie.authentication import ApiKeyAuthentication
from tastypie.models import ApiKey


class MetaBase:
    allowed_methods = ['get']
    filtering = {
        'site_domain': ALL,
        'channel_long_slug': ALL,
        'child_class': ALL,
        'tags': ALL,
    }


class ApiAuthentication(ApiKeyAuthentication):
    def __init__(self, method=[]):
        self.method = map(str.upper,method)

    def is_authenticated(self, request, **kwargs):
        try:
            if request.method in self.method or len(self.method) == 0:
                ApiKey.objects.get(
                    user__username=request.GET.get('username'),
                    key=request.GET.get('api_key'))
            return True
        except:
            ApiKey.DoesNotExist()
            return False

    def get_identifier(self, request):
        return request.user.username
