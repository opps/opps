#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

import os
import opps


install_requires = ["django",
                    "south>=0.7",
                    "Pillow==1.7.8",
                    "thumbor==3.7.1",
                    'django-thumbor==0.2',
                    "django-tagging==0.3.1",
                    "django-googl==0.1.1",
                    "django-wysiwyg-redactor==0.3.1",
                    "django-haystack==1.2.7",
                    "django-mptt==0.5.5",
                    "django-appconf"]
if 'OPPS_TRAVIS' in os.environ:
    install_requires.remove('south>=0.7')
    install_requires.remove('Pillow==1.7.8')
    install_requires.remove('thumbor==3.7.1')

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
        download_url="https://github.com/avelino/opps/tarball/master",
        license=opps.__license__,
        packages=find_packages(exclude=('doc', 'docs',)),
        namespace_packages=['opps'],
        package_dir={'opps': 'opps'},
        install_requires=install_requires,
        include_package_data=True,)
