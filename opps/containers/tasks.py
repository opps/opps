#!/usr/bin/env python
# -*- coding: utf-8 -*-
import celery


@celery.task
def check_mirror_site(container, Mirror):
    mirror_site = container.mirror_site.all()
    mirror_channel = container.mirror_channel.all()

    Mirror.objects.filter(
        container=container
    ).exclude(
        site__in=mirror_site
    ).exclude(
        channel__in=mirror_channel
    ).delete()

    for site in mirror_site:
        mirror, created = Mirror.objects.get_or_create(
            channel=container.channel,
            container=container,
            site=site,
            defaults=dict(
                container=container,
                user=container.user,
                title=container.title,
                published=container.published,
                slug=container.slug,
                channel_long_slug=container.channel.long_slug,
                channel_name=container.channel.name,
                main_image=container.main_image,
                hat=container.hat,
            )
        )

        if not created:
            mirror.title = container.title
            mirror.slug = container.slug
            mirror.published = container.published
            mirror.main_image = container.main_image
            mirror.channel_long_slug = container.channel.long_slug
            mirror.channel_name = container.channel.name
            mirror.site = site
            mirror.hat = container.hat
            mirror.save()


@celery.task
def check_mirror_channel(container, Mirror):
    mirror_channel = container.mirror_channel.all()

    if hasattr(container, "mirror_site"):
        mirror_site = container.mirror_site.all()
    else:
        mirror_site = []

    Mirror.objects.filter(
        container=container
    ).exclude(
        channel__in=mirror_channel
    ).exclude(
        site__in=mirror_site
    ).delete()

    for channel in mirror_channel:
        mirror, created = Mirror.objects.get_or_create(
            channel=channel,
            container=container,
            site=container.site,
            defaults=dict(
                container=container,
                user=container.user,
                title=container.title,
                published=container.published,
                slug=container.slug,
                channel_long_slug=channel.long_slug,
                channel_name=channel.name,
                main_image=container.main_image,
                hat=container.hat
            )
        )

        if not created:
            mirror.title = container.title
            mirror.slug = container.slug
            mirror.published = container.published
            mirror.main_image = container.main_image
            mirror.channel_long_slug = channel.long_slug
            mirror.channel_name = channel.name
            mirror.hat = container.hat
            mirror.save()
