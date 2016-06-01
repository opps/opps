# -*- coding: utf-8 -*-
import pkg_resources


pkg_resources.declare_namespace(__name__)

VERSION = (0, 2, 15)
__version__ = ".".join(map(str, VERSION))
__status__ = "Development"
__description__ = u"Open Source Content Management Platform - CMS for the "
u"magazines, newspappers websites and portals with "
u"high-traffic, using the Django Framework."

__author__ = u"Thiago Avelino"
__credits__ = ['Bruno Rocha']
__email__ = u"thiago@avelino.xxx"
__license__ = u"MIT"
__copyright__ = u"Copyright 2014, Thiago Avelino"
