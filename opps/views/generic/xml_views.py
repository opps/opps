# coding: utf-8

import xmltodict
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.detail import BaseDetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin


def cdata(data):
    if not data:
        return u""
    return u"<!CDATA[ {0} ]]>".format(data)


def response_mimetype(request):
    if "application/xml" in request.META['HTTP_ACCEPT']:
        return "application/xml"
    return "text/plain"


class XMLResponse(HttpResponse):
    """XML response class.
    takes a python dict and returns a XML string
    obj = {
        'results':
            {
                '@val': '1',
                'name': '3',
                '#text': 'sometext',
                'items': {'item': ['1', '2', '3']}
            }
    }
    in to --->
    <?xml version="1.0" encoding="utf-8"?>
    <results val="1">
        <name>3</name>
        <items>
           <item>1</item>
           <item>2</item>
           <item>3</item>
        </items>
        sometext
    </results>
    """
    def __init__(self, obj='', mimetype="application/xml", *args, **kwargs):
        content = xmltodict.unparse(obj)
        super(XMLResponse, self).__init__(content, mimetype, *args, **kwargs)


class XMLResponseMixin(object):
    """
    A mixin that can be used to render a XML response.
    """
    def render_to_xml_response(self, context, **response_kwargs):
        """
        Returns a XML response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_xml(context),
            content_type='application/xml',
            **response_kwargs
        )

        # response = XMLResponse(
        #     self.convert_context_to_xml(context),
        #     {},
        #     response_mimetype(self.request)
        # )
        # response['Content-Disposition'] = 'inline; filename=files.xml'

    def convert_context_to_xml(self, context):
        "Convert the context dictionary into a XML object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as XML.
        return xmltodict.unparse(context)


class XMLView(XMLResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_xml_response(context, **response_kwargs)


class XMLDetailView(XMLResponseMixin, BaseDetailView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_xml_response(context, **response_kwargs)


class HybridDetailView(XMLResponseMixin,
                       SingleObjectTemplateResponseMixin,
                       BaseDetailView):
    def render_to_response(self, context):
        # Look for a 'format=xml' GET argument
        if self.request.GET.get('format') == 'xml':
            return self.render_to_xml_response(context)
        else:
            return super(HybridDetailView, self).render_to_response(context)
