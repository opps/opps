#!/usr/bin/env python
# -*- coding: utf-8 -*-
from opps.api.conf import settings
from opps.views.generic.base import View


class BaseView(View):
    def get_paginate_by(self):
        return settings.OPPS_API_PAGINATE_BY
