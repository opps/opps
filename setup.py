#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from setuptools import setup, find_packages

import opps


REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
if sys.argv[1] == 'develop':
    REQUIREMENTS += [i.strip()
                     for i in open("requirements_dev.txt").readlines()]


dependency_links = [
    'http://github.com/avelino/django-googl/tarball/master#egg=django-googl',
    'http://github.com/opps/opps-piston/tarball/master#egg=opps-piston',
]

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Framework :: Django",
    "Framework :: Opps",
    'Programming Language :: Python',
    "Programming Language :: Python :: 2.7",
    "Operating System :: OS Independent",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules']

try:
    long_description = open('README.rst').read()
except:
    long_description = opps.__description__

setup(name='opps',
      version=opps.__version__,
      description=opps.__description__,
      long_description=long_description,
      classifiers=classifiers,
      keywords='opps cms django apps magazines websites',
      author=opps.__author__,
      author_email=opps.__email__,
      url='http://oppsproject.org',
      download_url="https://github.com/opps/opps/tarball/master",
      license=opps.__license__,
      packages=find_packages(exclude=('doc', 'docs', 'example')),
      namespace_packages=['opps'],
      package_dir={'opps': 'opps'},
      install_requires=REQUIREMENTS,
      dependency_links=dependency_links,
      scripts=['opps/bin/opps-admin.py'],
      include_package_data=True,
      test_suite='runtests',
      zip_safe=False)
