#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

import opps


install_requires = ["django",
                    "south>=0.7",
                    "Pillow==1.7.8",
                    "thumbor",
                    'libthumbor',
                    "django-googl==0.1.1",
                    "django-taggit",
                    "django-wysiwyg-redactor==0.3.1",
                    "django-haystack==1.2.7",
                    "django-mptt",
                    "django-appconf",
                    "python-memcached",
                    "johnny-cache"]
dependency_links = ['http://github.com/avelino/django-googl/tarball/master'
                    '#egg=django-googl',
                    'https://github.com/jmoiron/johnny-cache/tarball/master'
                    '#egg=johnny-cache']

classifiers = ["Development Status :: 4 - Beta",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Framework :: Django",
               'Programming Language :: Python',
               "Programming Language :: Python :: 2.7",
               "Programming Language :: Python :: 2.6",
               "Operating System :: OS Independent",
               "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
               'Topic :: Software Development :: Libraries :: Python Modules']

try:
    long_description = open('README.md').read()
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
      packages=find_packages(exclude=('doc', 'docs',)),
      namespace_packages=['opps'],
      package_dir={'opps': 'opps'},
      install_requires=install_requires,
      dependency_links=dependency_links,
      scripts=['opps/bin/opps-admin.py'],
      include_package_data=True,)
