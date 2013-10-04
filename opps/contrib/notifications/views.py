#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from opps.views.generic.detail import DetailView
from opps.views.generic.list import ListView
from opps.views.generic.json_views import JSONPResponse
from opps.db import Db

from .models import Notification


class AsyncServer(DetailView):
    model = Notification

    def _queue(self):
        _db = Db(self.get_object.get_absolute_url(),
                 self.get_object().id)
        pubsub = _db.object().pubsub()
        pubsub.subscribe(_db.key)

        while True:
            for m in pubsub.listen():
                if m['type'] == 'message':
                    yield u"data: {}\n\n".format(m['data'])
            yield u"data: {}\n\n".format(json.dumps({"action": "ping"}))
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

    def get_queryset(self):
        query = super(LongPullingServer, self).get_queryset()
        old_id = self.request.GET.get('old_id', 0)
        return query.filter(id__gte=old_id)._clone()
