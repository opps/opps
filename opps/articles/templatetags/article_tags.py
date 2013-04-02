# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils import timezone

from .models import ArticleBox


register = template.Library()


@register.simple_tag
def get_articlebox(slug, channel_slug=None, template_name=None):
    if channel_slug:
        slug = "{0}-{1}".format(slug, channel_slug)

    try:
        box = ArticleBox.objects.get(site=settings.SITE_ID, slug=slug,
                                     date_available__lte=timezone.now(),
                                     published=True)
    except ArticleBox.DoesNotExist:
        box = None

    t = template.loader.get_template('articles/articlebox_detail.html')
    if template_name:
        t = template.loader.get_template(template_name)

    return t.render(template.Context({'articlebox': box, 'slug': slug}))


@register.simple_tag
def get_all_articlebox(channel_slug, template_name=None):
    boxes = ArticleBox.objects.filter(site=settings.SITE_ID,
                                      date_available__lte=timezone.now(),
                                      published=True,
                                      channel__slug=channel_slug)

    t = template.loader.get_template('articles/articlebox_list.html')
    if template_name:
        t = template.loader.get_template(template_name)

    return t.render(template.Context({'articleboxes': boxes}))
