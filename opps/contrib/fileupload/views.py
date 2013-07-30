# coding: utf-8
import random

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

from opps.images.models import Image
from opps.containers.models import Container, ContainerImage
from opps.sources.models import Source
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

        source = request.POST.get('source', None)
        if source:
            qs = Source.objects.filter(name=source, site=container.site)
            if qs:
                source = qs[0]
            else:
                source = Source.objects.create(
                    name=source,
                    slug=slugify(source),
                    user=request.user,
                    published=True
                )

        slug = slugify(title)
        slug = "{0}-{1}".format(slug[:100], random.getrandbits(32))

        instance = Image(
            site=container.site,
            user=container.user,
            date_available=container.date_available,
            title=title,
            slug=slug,
            image=f,
            published=True,
        )
        if source:
            instance.source = source

        instance.save()

        order = request.POST.get('order', 0)
        ContainerImage.objects.create(
            container=container,
            image=instance,
            caption=caption,
            order=int(order)
        )

        data = [{'name': f.name,
                 'url': "%s" % instance.image.url,
                 'thumbnail_url': "%s" % image_url(
                     instance.image.url,
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
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)
