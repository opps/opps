#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, time
from django.http import HttpResponse, Http404
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from opps.api.views.generic.list import ListView as ListAPIView
from opps.api.views.generic.list import ListCreateView
from opps.views.generic.list import ListView
from opps.views.generic.detail import DetailView
from opps.db import Db

from .models import Notification


class SSEServer(DetailView):
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


