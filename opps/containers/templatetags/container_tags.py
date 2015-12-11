# -*- coding: utf-8 -*-
from collections import Counter
import logging

from django import template
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.core.cache import cache
from django.contrib.sites.models import Site

from opps.channels.models import Channel
from opps.contrib.middleware.global_request import get_request
from opps.containers.models import Container, ContainerBox, Mirror

from magicdate import magicdate


register = template.Library()
logger = logging.getLogger()


@register.assignment_tag
def get_tags_counter(queryset=None, n=None):
    if queryset is None:
        queryset = Container.objects.all_published()

    counter = Counter()
    qs = queryset.filter(tags__isnull=False).exclude(tags="").order_by()
    print qs.count()
    for tags in qs.values_list("tags", flat=True).distinct():
        l = [i.strip() for i in tags.split(",") if i.strip()]
        counter.update(l)

    return counter.most_common(n)


@register.filter
def values_list_flat(queryset, field='pk'):
    return queryset.values_list(field, flat=True)


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


@register.assignment_tag(takes_context=True)
def load_boxes(context, slugs=None, **filters):
    if slugs:
        filters['slug__in'] = ordered_slugs = slugs.split(',')

    request = context['request']
    current_site = getattr(
        request,
        'site',
        Site.objects.get(pk=settings.SITE_ID)
    )

    filters['site__in'] = [current_site]
    master_site = settings.OPPS_CONTAINERS_SITE_ID or 1
    if current_site.id != master_site:
        filters['site__in'].append(master_site)

    filters['date_available__lte'] = timezone.now()
    filters['published'] = True

    boxes = ContainerBox.objects.filter(**filters).order_by('-site')
    fallback = getattr(settings, 'OPPS_MULTISITE_FALLBACK', False)

    exclude_ids = []

    if slugs:
        def ob(i, o=ordered_slugs):
            return (i.site_id != current_site, i.site_id, o.index(i.slug))

        boxes = sorted(boxes, key=ob, reverse=True)

    for box in boxes:
        if box.queryset:
            results = box.get_queryset(exclude_ids=exclude_ids)
        else:
            results = box.ordered_containers(exclude_ids=exclude_ids)

        if box.queryset:
            for i in results:
                if i.pk not in exclude_ids and isinstance(i, Container):
                    exclude_ids.append(i.pk)
        elif fallback:
            for i in results:
                if i.container_id and i.container_id not in exclude_ids:
                    exclude_ids.append(i.container_id)
        else:
            for i in results:
                if i.pk not in exclude_ids:
                    exclude_ids.append(i.pk)

    results = {}
    for box in boxes:
        if box.slug not in results:
            results[box.slug] = box

    get_request().container_boxes = results
    return results


@register.simple_tag(takes_context=True)
def get_containerbox(
        context, slug, template_name=None, channel=None, **extra_context):

    request = context['request']
    current_site = getattr(
        request,
        'site',
        Site.objects.get(pk=settings.SITE_ID)
    )
    is_mobile = getattr(request, 'is_mobile', False)

    cachekey = "ContainerBox-{0}-{1}-{2}-{3}".format(
        slug,
        template_name,
        is_mobile,
        current_site.id
    )

    render = cache.get(cachekey)
    if render:
        return render

    box = getattr(get_request(), 'container_boxes', {}).get(slug, None)

    if not box:
        filters = {}
        filters['site_id'] = current_site.id
        filters['slug'] = slug
        filters['date_available__lte'] = timezone.now()
        filters['published'] = True
        if channel is not None:
            filters['channel'] = channel

        master_site = settings.OPPS_CONTAINERS_SITE_ID or 1

        try:
            box = ContainerBox.objects.get(**filters)
        except ContainerBox.DoesNotExist:
            box = None

        if current_site.id != master_site and \
           not box or not getattr(box, 'has_content', False):
            filters['site_id'] = master_site
            try:
                box = ContainerBox.objects.get(**filters)
            except ContainerBox.DoesNotExist:
                box = None

        if not box:
            box = ContainerBox.objects.none()

    t = template.loader.get_template('articles/articlebox_detail.html')
    if template_name:
        t = template.loader.get_template(template_name)

    context = {
        'articlebox': box,
        'slug': slug,
        'context': context,
        'request': request
    }

    context.update(extra_context)

    render = t.render(template.Context(context))

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

    cachekey = "get_all_containerbox-{0}-{1}".format(
        channel_long_slug,
        template_name)

    render = cache.get(cachekey)
    if render:
        return render

    filters = {}
    filters['date_available__lte'] = timezone.now()
    filters['published'] = True
    filters['site'] = settings.SITE_ID
    if settings.OPPS_CONTAINERS_SITE_ID:
        filters['site'] = settings.OPPS_CONTAINERS_SITE_ID

    boxes = ContainerBox.objects.filter(**filters)

    if channel_long_slug:
        boxes = boxes.filter(channel_long_slug=channel_long_slug)

    t = template.loader.get_template('articles/articlebox_list.html')
    if template_name:
        t = template.loader.get_template(template_name)

    render = t.render(template.Context({'articleboxes': boxes}))
    cache.set(cachekey, render, settings.OPPS_CACHE_EXPIRE)

    return render


@register.simple_tag
def get_post_content(post, template_name='containers/post_related.html',
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

    # Fix embed allowfullscreen
    # TinyMCE BUG
    content = content.replace('allowfullscreen="allowfullscreen"',
                              'allowfullscreen="true"')

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
            _url = 'http://{0}{1}'.format(
                obj.site,
                obj.get_absolute_url())
        if url_only:
            return _url
        return 'href="{0}" target="{1}"'.format(_url, _target)
    except Exception as e:
        logger.error("Exception at templatetag get_url: {0}".format(e))
        return obj.get_absolute_url()


@register.assignment_tag
def get_containers_by(limit=None, **filters):
    """Return a list of containers filtered by given args"""
    cachekey = u'getcontainersby-{0}'.format(hash(frozenset(filters.items())))
    _cache = cache.get(cachekey)
    if _cache:
        return _cache

    site = settings.SITE_ID
    if settings.OPPS_CONTAINERS_SITE_ID:
        site = settings.OPPS_CONTAINERS_SITE_ID

    qs = Container.objects.all_published()
    qs = qs.filter(site=site, **filters)
    qs = qs[:limit]
    containers = [i for i in qs]

    cache.set(cachekey, containers, settings.OPPS_CACHE_EXPIRE)
    return containers


@register.assignment_tag
def filter_queryset_by(queryset, **filters):
    """Filter object list"""
    if not getattr(queryset, 'query', False):
        return queryset

    cachekey = u'filterquerysetby-{0}'.format(hash(unicode(queryset.query)))
    _cache = cache.get(cachekey)
    if _cache:
        return _cache

    # check for __in lookups and split the param
    found_in_lookup = None
    for key in filters.keys():
        if '__in' in key:
            found_in_lookup = key

    if found_in_lookup:
        filters[found_in_lookup] = filters[found_in_lookup].split(',')

    if not queryset.query.can_filter():
        # create new queryset based on the ids and apply filter
        ids = [i.id for i in queryset]
        queryset = queryset.model.objects.filter(id__in=ids).filter(**filters)
        return queryset

    containers = queryset.filter(**filters)
    cache.set(cachekey, containers, settings.OPPS_CACHE_EXPIRE)
    return containers


@register.assignment_tag
def exclude_queryset_by(queryset, **excludes):
    """Exclude object list"""

    if not getattr(queryset, 'query', False):
        return queryset

    cachekey = u'excludequerysetby-{0}'.format(hash(unicode(queryset.query)))
    _cache = cache.get(cachekey)
    if _cache:
        return _cache

    # check for __in lookups and split the param
    found_in_lookup = None
    for key in excludes.keys():
        if '__in' in key:
            found_in_lookup = key

    if found_in_lookup:
        excludes[found_in_lookup] = excludes[found_in_lookup].split(',')

    if not queryset.query.can_filter():
        # create new queryset based on the ids and apply filter
        ids = [i.id for i in queryset]
        containers = queryset.model.objects.filter(id__in=ids).exclude(
            **excludes
        )
    else:
        containers = queryset.exclude(**excludes)

    if 'child_class' in excludes:
        # we need to exclude the mirrors containing the child_class that
        # we want to exclude
        bad_child_class = excludes['child_class']
        mirrors = Mirror.objects.filter(
            container__child_class=bad_child_class
        ).values_list('id', flat=True)
        if mirrors:
            containers = containers.exclude(pk__in=mirrors)

    cache.set(cachekey, containers, settings.OPPS_CACHE_EXPIRE)
    return containers


@register.assignment_tag
def get_container_by_channel(slug, number=10, depth=1,
                             include_children=True, **kwargs):
    box = None
    magic_date = kwargs.pop('magic_date', False)
    date = timezone.now()

    if magic_date:
        try:
            date = magicdate(magic_date)
        except Exception:
            pass

    # __in split treatment
    splited = dict([
        (key, value.split(','))
        for key, value
        in kwargs.items()
        if key.endswith('__in') and type(value) is not list])
    kwargs.update(splited)

    if include_children:
        k = 'channel_id__in'
        kwargs[k] = cache.get(
            'get_container_by_channel-{0}'.format(slug))
        if not kwargs[k]:

            try:
                channel = Channel.objects.get(long_slug=slug)
                qs = channel.get_descendants(include_self=True)
                qs = qs.filter(level__lte=channel.level + depth)
                kwargs[k] = \
                    qs.values_list("id", flat=True)
                cache.set(
                    'get_container_by_channel-{0}'.format(slug),
                    kwargs[k],
                    settings.OPPS_CACHE_EXPIRE)

            except Channel.DoesNotExist:
                kwargs[k] = []

    try:
        kwargs['site'] = settings.SITE_ID
        if settings.OPPS_CONTAINERS_SITE_ID:
            kwargs['site'] = settings.OPPS_CONTAINERS_SITE_ID
        kwargs['show_on_root_channel'] = include_children
        kwargs['date_available__lte'] = date
        kwargs['published'] = True
        box = Container.objects.distinct().filter(
            **kwargs).order_by('-date_available')[:number]
    except:
        pass
    return box


@register.assignment_tag
def get_containerbox_by(**filters):
    """Return a list of containers filtered by given args"""
    site = settings.SITE_ID
    if settings.OPPS_CONTAINERS_SITE_ID:
        site = settings.OPPS_CONTAINERS_SITE_ID
    return ContainerBox.objects.filter(site=site,
                                       published=True,
                                       date_available__lte=timezone.now(),
                                       **filters)


@register.simple_tag(takes_context=True)
def get_containerbox_list(context, slug, num=0, template_name=None):
    """ returns a list of sub-lists of the containerbox specific containers,
        the size of the sub lists is treated with a parameter num """

    request = context['request']

    cachekey = "ContainerBoxList-{0}-{1}-{2}".format(
        slug,
        template_name,
        request.is_mobile,
    )

    render = cache.get(cachekey)
    if render:
        return render

    site = settings.SITE_ID
    if settings.OPPS_CONTAINERS_SITE_ID:
        site = settings.OPPS_CONTAINERS_SITE_ID
    try:
        box = ContainerBox.objects.filter(
            site=site, slug=slug,
            date_available__lte=timezone.now(),
            published=True)
        if isinstance(num, int) and num > 0 and box:
            list_box = box[0].ordered_box_containers()
            box = [list_box[i:i + num] for i in range(0, len(list_box), num)]
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


@register.assignment_tag
def get_custom_field_value(obj, field_slug):
    """
    Return a custom field value
    """
    if not callable(getattr(obj, 'custom_fields')):
        return None

    if not obj.custom_fields():
        return None

    return obj.custom_fields().get(field_slug)


@register.assignment_tag
def get_postrelated_by(obj, **filters):
    """Return a list of post related filtered by given args"""
    if getattr(obj, 'postrelated_post', False):
        cachekey = u'getpostrelatedby-{0}-{1}'.format(
            hash(frozenset(filters.items())), obj.pk)

        _cache = cache.get(cachekey)

        if _cache:
            return _cache

        queryset = obj.postrelated_post.filter(post__pk=obj.pk)

        if 'exclude' in filters.keys():
            del filters['exclude']
            containers = [i.related for i in queryset.exclude(**filters)
                                                     .order_by('order')]
        else:
            containers = [i.related for i in queryset.filter(**filters)
                                                     .order_by('order')]

        cache.set(cachekey, containers, settings.OPPS_CACHE_EXPIRE)
        return containers
    return ''
