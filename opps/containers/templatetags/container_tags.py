# -*- coding: utf-8 -*-
import logging

from django import template
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.template.defaultfilters import linebreaksbr
from django.core.cache import cache

from opps.containers.models import Container, ContainerBox
from opps.channels.models import Channel


register = template.Library()
logger = logging.getLogger()


@register.assignment_tag
def get_recommendations(query_slice, child_class, container):
    """
    Takes the container object and get recommendations and filters by given
    child_class and limit the result by given slice.

    Sample usage::

        {% get_recommendations ":3" "post" container as context_var %}

    query_slice:
        A string with slice notation to limit the queryset result
    child_class:
        Name of child class
    container:
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

    return container.recommendation(child_class, bits)


@register.simple_tag(takes_context=True)
def get_containerbox(context, slug, template_name=None):

    cachekey = "ContainerBox-{}-{}".format(
        slug,
        template_name)

    render = cache.get(cachekey)
    if render:
        return render

    try:
        box = ContainerBox.objects.get(site=settings.SITE_ID, slug=slug,
                                       date_available__lte=timezone.now(),
                                       published=True)
    except ContainerBox.DoesNotExist:
        box = None

    t = template.loader.get_template('articles/articlebox_detail.html')
    if template_name:
        t = template.loader.get_template(template_name)

    render = t.render(template.Context({
        'articlebox': box,
        'slug': slug,
        'context': context}
    ))

    cache.set(cachekey, render, settings.OPPS_CACHE_EXPIRE)

    return render


@register.simple_tag
def get_all_containerbox(channel_long_slug=None, template_name=None):
    """
    Takes all containers or containers that match the channel name (long slug).

    Sample usages::

        {% get_all_containerbox "channel" template_name='my_template.html' %}
        {% get_all_containerbox "channel/subchannel" %}
        {% get_all_containerbox %}

    channel_long_slug:
        Long path to channel (including subchannel if is the case)
    """

    cachekey = "get_all_containerbox-{}-{}".format(
        channel_long_slug,
        template_name)

    render = cache.get(cachekey)
    if render:
        return render

    boxes = ContainerBox.objects.filter(
        site=settings.SITE_ID,
        date_available__lte=timezone.now(),
        published=True)

    if channel_long_slug:
        boxes = boxes.filter(
            channel_long_slug=channel_long_slug)

    t = template.loader.get_template('articles/articlebox_list.html')
    if template_name:
        t = template.loader.get_template(template_name)

    render = t.render(template.Context({'articleboxes': boxes}))
    cache.set(cachekey, render, settings.OPPS_CACHE_EXPIRE)

    return render


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

    # REMOVE NEW LINES
    content = linebreaksbr(content)

    if not get_related:
        return content

    related_posts = getattr(post, related_name, None)

    if not related_posts.exists():
        return mark_safe(content)

    # GET THE TEMPLATE
    t = template.loader.get_template(template_name)
    related_rendered = t.render(template.Context({
        'post': post, related_name: related_posts}))
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


@register.assignment_tag
def get_containers_by(limit=None, **filters):
    """Return a list of containers filtered by given args"""
    cachekey = hash(frozenset(filters.items()))
    _cache = cache.get(cachekey)
    if _cache:
        return _cache
    containers = [i for i in Container.objects.filter(
        site=settings.SITE_ID, published=True, **filters)[:limit]]
    cache.set("getconby-{}".format(cachekey), 3600)
    return containers


@register.assignment_tag
def get_container_by_channel(slug, number=10, depth=1,
                             include_children=True, **kwargs):
    box = None
    if include_children:
        try:
            kwargs['channel_long_slug__in'] = cache.get(
                'get_container_by_channel-{}'.format(slug))
            if not kwargs['channel_long_slug__in']:
                base_channel = Channel.objects.get(long_slug=slug)
                kwargs['channel_long_slug__in'] = [base_channel.long_slug]

                def _append_recursivelly(channel, current_level=0):
                    # Depth test
                    if current_level >= depth:
                        return
                    elif current_level < depth:
                        current_level += 1

                    for children in channel.get_children():
                        kwargs['channel_long_slug__in'].append(
                            children.long_slug)
                        # Recursion
                        _channel = Channel.objects.get(
                            long_slug=children.long_slug)
                        _append_recursivelly(_channel, current_level)

                _append_recursivelly(base_channel)
                cache.set('get_container_by_channel-{}'.format(slug),
                          kwargs['channel_long_slug__in'],
                          settings.OPPS_CACHE_EXPIRE)
        except Channel.DoesNotExist:
            kwargs['channel_long_slug__in'] = []
    try:
        kwargs['site'] = settings.SITE_ID
        kwargs['show_on_root_channel'] = include_children
        kwargs['date_available__lte'] = timezone.now()
        kwargs['published'] = True
        box = Container.objects.distinct().filter(
            **kwargs).order_by('-date_available')[:number]
    except:
        pass
    return box


@register.assignment_tag
def get_containerbox_by(**filters):
    """Return a list of containers filtered by given args"""
    return ContainerBox.objects.filter(site=settings.SITE_ID,
                                       published=True,
                                       date_available__lte=timezone.now(),
                                       **filters)


@register.simple_tag(takes_context=True)
def get_containerbox_list(context, slug, num=0, template_name=None):
    """ returns a list of sub-lists of the containerbox specific containers,
        the size of the sub lists is treated with a parameter num """

    cachekey = "ContainerBoxList-{}-{}".format(
        slug,
        template_name)

    render = cache.get(cachekey)
    if render:
        return render

    try:
        box = ContainerBox.objects.filter(site=settings.SITE_ID, slug=slug,
                                       date_available__lte=timezone.now(),
                                       published=True)
        if isinstance(num, int) and num > 0:
            list_box = box[0].ordered_box_containers()
            box = [list_box[i:i+num] for i in range(0,len(list_box),num)]
    except ContainerBox.DoesNotExist:
        box = None

    t = template.loader.get_template('articles/articlebox_container_list.html')
    if template_name:
        t = template.loader.get_template(template_name)

    render = t.render(template.Context({
        'list_container': box,
        'slug': slug,
        'context': context}
    ))

    cache.set(cachekey, render, settings.OPPS_CACHE_EXPIRE)

    return render
