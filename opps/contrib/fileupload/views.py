#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import json

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

from opps.images.models import Image
from opps.containers.models import Container, ContainerImage
from opps.images.generate import image_url


def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    return "text/plain"


@csrf_exempt
@login_required(login_url='/admin/')
def image_create(request, container_pk):

    container = get_object_or_404(Container, pk=int(container_pk))
    if request.method == "POST":
        f = request.FILES.get('image')

        title = request.POST.get('title') or container.title
        caption = request.POST.get('caption', '')
        source = request.POST.get('source', '')
        tags = request.POST.get('tags', '')
        slug = slugify(title)
        slug = "{0}-{1}".format(slug[:100], random.getrandbits(32))

        instance = Image(
            site=container.site,
            user=container.user,
            date_available=container.date_available,
            title=title,
            slug=slug,
            archive=f,
            source=source,
            published=True,
            tags=tags,
        )
        instance.save()

        order = request.POST.get('order', 0)
        ContainerImage.objects.create(
            container=container,
            image=instance,
            caption=caption,
            order=int(order)
        )

        data = [{'name': f.name,
                 'url': "%s" % instance.archive.url,
                 'thumbnail_url': "%s" % image_url(
                     instance.archive.url,
                     width=60,
                     height=60
                 ),
                 "delete_url": "",
                 "delete_type": "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    else:
        return render(request, 'fileupload/image_form.html',
                      {'container': container})


class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self, obj='', json_opts={}, mimetype="application/json",
                 *args, **kwargs):
        content = json.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)
