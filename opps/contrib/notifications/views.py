#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
from django.conf import settings
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from opps.views.generic.list import ListView
from opps.views.generic.json_views import JSONPResponse
from opps.db import Db

from .models import Notification


class AsyncServer(ListView):
    model = Notification

    def _db(self, obj):
        _db = Db(
            obj.container.get_absolute_url(),
            obj.container.id)
        pubsub = _db.object().pubsub()
        pubsub.subscribe(_db.key)
        return pubsub

    def _queue(self):
        try:
            obj = self.get_queryset()[0]
        except:
            obj = False

        if not obj:
            while True:
                msg = u"compatibility: true\n"
                msg += u"retry: 10000\n"
                msg += u"data: {0}\n\n".format(
                    json.dumps({"action": "error"}))
                yield msg
                time.sleep(10)
        else:
            while True:
                pubsub = self._db(obj)
                for m in pubsub.listen():
                    if m['type'] == 'message':
                        msg = u"compatibility: true\n"
                        msg += u"retry: 10000\n"
                        msg += u"data: {0}\n\n".format(m['data'])
                        yield msg
                ping = u"compatibility: true\n"
                ping += u"retry: 10000\n"
                ping += u"data: {0}\n\n".format(
                    json.dumps({"action": "ping"}))
                yield ping
                time.sleep(0.5)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        response = StreamingHttpResponse(self._queue(),
                                         mimetype='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['Software'] = 'opps-liveblogging'
        response['Access-Control-Allow-Origin'] = '*'
        response.flush()
        return response


class LongPullingServer(ListView, JSONPResponse):
    model = Notification

    def get_template_names(self):
        templates = []
        domain_folder = self.get_template_folder()

        if not self.long_slug:
            templates.append('{0}/none.json'.format(domain_folder))
            return templates

        list_name = 'list'

        if self.template_name_suffix:
            list_name = "{0}{1}".format(list_name, self.template_name_suffix)

        if self.channel:
            # Check layout, change via admin
            if self.channel.layout != u'default':
                list_name = self.channel.layout

            if self.channel.group and self.channel.parent:
                templates.append('{0}/{1}/{2}.json'.format(
                    domain_folder, self.channel.parent.long_slug, list_name))

                if self.request.GET.get('page') and\
                   self.__class__.__name__ not in\
                   settings.OPPS_PAGINATE_NOT_APP:
                    templates.append('{0}/{1}/{2}_paginated.json'.format(
                        domain_folder, self.channel.parent.long_slug,
                        list_name))

            if self.request.GET.get('page') and\
               self.__class__.__name__ not in settings.OPPS_PAGINATE_NOT_APP:
                templates.append('{0}/{1}/{2}_paginated.json'.format(
                    domain_folder, self.channel.long_slug, list_name))

            templates.append('{0}/{1}/{2}.json'.format(
                domain_folder, self.channel.long_slug, list_name))

            for t in self.channel.get_ancestors()[::-1]:
                templates.append('{0}/{1}/{2}.json'.format(
                    domain_folder, t.long_slug, list_name))
                if self.request.GET.get('page') and\
                   self.__class__.__name__ not in\
                   settings.OPPS_PAGINATE_NOT_APP:
                    templates.append('{0}/{1}/{2}_paginated.json'.format(
                        domain_folder, t.long_slug, list_name))

        if self.request.GET.get('page') and\
           self.__class__.__name__ not in settings.OPPS_PAGINATE_NOT_APP:
            templates.append('{0}/{1}_paginated.json'.format(domain_folder,
                                                             list_name))

        templates.append('{0}/{1}.json'.format(domain_folder, list_name))
        return templates

    def get_queryset(self):
        query = super(LongPullingServer, self).get_queryset()
        old_id = self.request.GET.get('old_id', 0)
        return query.filter(id__gte=old_id)._clone()
