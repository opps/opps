#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libthumbor import CryptoURL
from django.conf import settings


crypto = CryptoURL(key=settings.THUMBOR_SECURITY_KEY)


def _remove_prefix(url, prefix):
    if url.startswith(prefix):
        return url[len(prefix):]
    return url


def _remove_schema(url):
    return _remove_prefix(url, 'http://')


def _prepend_media_url(url):
    if url.startswith(settings.MEDIA_URL):
        url = _remove_prefix(url, settings.MEDIA_URL)
        url.lstrip('/')
        return u'{0}/{1}'.format(settings.THUMBOR_MEDIA_URL, url)
    return url


def image_url(image_url, **kwargs):
    if not settings.THUMBOR_ENABLED:
        return image_url

    image_url = _prepend_media_url(image_url)
    image_url = _remove_schema(image_url)

    try:
        encrypted_url = crypto.generate(
            image_url=image_url,
            **dict(settings.THUMBOR_ARGUMENTS, **kwargs)).strip('/')
        return u'{0}/{1}'.format(settings.THUMBOR_SERVER, encrypted_url)
    except:
        return u""
