#!/usr/bin/env python
# -*- coding: utf-8 -*-
import celery


@celery.task
def check_mirror_channel(container, Mirror):
    mirror_channel = container.mirror_channel.all()

    Mirror.objects.filter(
        container=container
    ).exclude(channel__in=mirror_channel).delete()

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
                main_image=container.main_image
            )
        )

        if not created:
            mirror.title = container.title
            mirror.slug = container.slug
            mirror.published = container.published
            mirror.main_image = container.main_image
            mirror.channel_long_slug = channel.long_slug
            mirror.channel_name = channel.name
            mirror.save()
