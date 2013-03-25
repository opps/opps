# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from opps.article.models import ArticleBox


register = template.Library()

@register.inclusion_tag('article/articlebox_detail.html')
def get_articlebox(slug, channel_slug=None):
    if channel_slug:
        slug = slug + '-' + channel_slug

    try:
        box = ArticleBox.objects.get(site=settings.SITE_ID, slug=slug)
    except ArticleBox.DoesNotExist:
        box = None

    return {'articlebox': box}


@register.inclusion_tag('article/articlebox_list.html')
def get_all_articlebox(channel_slug):
    boxes = ArticleBox.objects.filter(site=settings.SITE_ID, channel__slug=channel_slug)
    return {'articleboxes': boxes}
