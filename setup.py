#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

import opps



install_requires = ["Django>=1.5",
                    "south>=0.7",
                    "Pillow==1.7.8",
                    "django-filebrowser==3.5.1",
                    "django-redis",
                    "django-redactor"]

classifiers = ["Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Framework :: Django",
    'Programming Language :: Python',
    "Programming Language :: Python :: 2.7",
    "Operating System :: OS Independent",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    'Topic :: Software Development :: Libraries :: Python Modules',]

try:
    long_description = open('README.md').read()
except:
    long_description = opps.__description__

setup(name='opps',
    version = opps.__version__,
    description = opps.__description__,
    long_description = long_description,
    classifiers = classifiers,
    keywords = 'opps cms django apps magazines websites',
    author = opps.__author__,
    author_email = opps.__email__,
    url = 'http://oppsproject.org',
    download_url = "https://github.com/avelino/opps/tarball/master",
    license = opps.__license__,
    packages = find_packages(exclude=('doc',)),
    package_dir = {'opps': 'opps'},
    install_requires = install_requires,
    include_package_data = True,
)

