# -*- coding: utf-8 -*-
import warnings
from threading import current_thread


class FakeRequest(object):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            ("You must include "
             "opps.contrib.middleware.global_request.GlobalRequest"
             " as the last one in MIDDLEWARE_CLASSES")
        )


class GlobalRequest(object):
    """Thread-safe middleware that makes current request available globally

    Reference: https://djangosnippets.org/snippets/2853/

    """
    _requests = {}

    @staticmethod
    def get_request():
        try:
            return GlobalRequest._requests[current_thread()]
        except KeyError:
            return FakeRequest()

    def process_request(self, request):
        GlobalRequest._requests[current_thread()] = request

    def process_response(self, request, response):
        # Cleanup
        thread = current_thread()
        try:
            del GlobalRequest._requests[thread]
        except KeyError:
            pass
        return response


def get_request():
    return GlobalRequest.get_request()
