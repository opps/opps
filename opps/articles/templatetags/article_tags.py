# -*- coding: utf-8 -*-
import logging

from django import template
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe

from opps.containers.models import Container
from opps.containers.models import ContainerBox


register = template.Library()
logger = logging.getLogger()


@register.simple_tag(takes_context=True)
def get_articlebox(context, slug, template_name=None):

    try:
        box = ContainerBox.objects.get(site=settings.SITE_ID, slug=slug,
                                       date_available__lte=timezone.now(),
                                       published=True)
    except ContainerBox.DoesNotExist:
        box = None

    t = template.loader.get_template('articles/articlebox_detail.html')
    if template_name:
        t = template.loader.get_template(template_name)

    return t.render(template.Context({
        'articlebox': box,
        'slug': slug,
        'context': context}
    ))


@register.simple_tag
def get_all_articlebox(channel_long_slug, template_name=None):
    boxes = ContainerBox.objects.filter(
        site=settings.SITE_ID,
        date_available__lte=timezone.now(),
        published=True,
        channel_long_slug=channel_long_slug)

    t = template.loader.get_template('articles/articlebox_list.html')
    if template_name:
        t = template.loader.get_template(template_name)

    return t.render(template.Context({'articleboxes': boxes}))


@register.simple_tag
def get_post_content(post, template_name='articles/post_related.html',
                     content_field='content', related_name='related_posts',
                     get_related=True, safe=True, divider="<br />",
                     placeholder=settings.OPPS_RELATED_POSTS_PLACEHOLDER):
    """
    takes the post and tries to find the related posts to embed inside
    the content, if not found return only the content.

    post:
        Post instance
    template_name:
        path to template which receives the related posts
    content_field:
        name of the field with post content
    related_name:
        a m2m field name or a @property name which
        returns a queryset of related posts
    get_related:
        if False bypass and return only the content
    safe:
        if True mark the content as safe
    divider:
        used when there is no placeholder
    placeholder:
        the string to replace ex: --related--
    """
    if not hasattr(post, content_field):
        return None
    content = getattr(post, content_field, '')
    if not get_related:
        return content

    related_posts = getattr(post, related_name, None)

    if not related_posts.exists():
        return mark_safe(content)

    # GET THE TEMPLATE
    t = template.loader.get_template(template_name)
    related_rendered = t.render(
        template.Context({'post': post, related_name: related_posts})
    )
    # EMBED RELATED POSTS
    if placeholder in content:
        return mark_safe(content.replace(
            placeholder,
            related_rendered
        ))
    else:
        return mark_safe(content + divider + related_rendered)


@register.simple_tag
def get_url(obj, http=False, target=None, url_only=False):

    if not hasattr(obj, 'child_class'):
        return obj.get_absolute_url()

    try:
        _url = obj.get_absolute_url()
        _target = target or '_self'
        _is_link = obj.child_class == 'Link'
        # Determine if it's a local or foreign link
        if _is_link and not obj.link.is_local() and not target:
            _target = '_blank'
        # Determine url type
        if http:
            _url = 'http://{}{}'.format(
                obj.site,
                obj.get_absolute_url())
        if url_only:
            return _url
        return 'href="{}" target="{}"'.format(_url, _target)
    except Exception as e:
        logger.error("Exception at templatetag get_url: {}".format(e))
        return obj.get_absolute_url()


@register.assignment_tag(takes_context=True)
def get_related(context, query_slice, chield_class, related_object):
    """
    Takes the related object and search by related posts and filters by given
    child_class and limit the result by given slice.

    Sample usage::

        {% get_related ":3" "post" context %}

    query_slice:
        A string with slice notation to limit the queryset result
    chield_class:
        Name of child class
    related_object:
        A Container object
    """

    if not query_slice:
        query_slice = ":"

    bits = []
    for x in query_slice.split(':'):
        if len(x) == 0:
            bits.append(None)
        else:
            bits.append(int(x))

    return Container.objects.filter(site=settings.SITE_ID,
                                    date_available__lte=timezone.now(),
                                    published=True,
                                    child_class=chield_class,
                                    post_relatedposts=related_object)[slice(*bits)]
