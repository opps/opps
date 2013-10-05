Overview
========

Dependencies
------------

Opps makes use of as few libraries as possible (apart from a standard Django environment), with the following dependencies

* Python 2.7
* Django >= 1.5
* Python Imaging Library - for image resizing
* South - for database migrations
* Django Taggit
* Django Mptt


Features
--------

* Write in Django
* Containar manager (**container** is content type in *Opps CMS*)
* * Save draft and and preview
* * Dynamic custom field, add field in specific container
* WYSIWYG editing (more one option)
* Container Box manager (Custom channel home page, add dynamic/fix box)
* Channel organize via tree (via mptt, not level limit)
* Media file manager, default manager images
* * Multi upload
* User permission in Admin, manager site access on admin
* SEO friendly URLs and meta data
* Configurable dashboard (used grappelli admin theme)
* API for custom container types
* Search engine
* Multi-Site
* JVM compatible (via Jython)
* .NET Framework compatible (via IronPython)


Browser Support
---------------

Opps’s admin (used Bootstrap Twitter) interface works with all modern browsers.


Language Translations
---------------------

Opps makes full use of translation strings, which allow Opps to be translated into multiple languages using Django’s internationalization methodology. 
Translations are managed on the `Transiflex <https://www.transifex.com/projects/p/opps/>`_ website but can also be submitted via `GitHub <https://github.com/opps/opps>`_. Consult the documentation for Django’s internationalization methodology for more information on creating translations and using them.


Sites Using Opps
----------------

* `Portal Virgula <http://virgula.uol.com.br>`_
* `Portal Guiame <http://guiame.com.br>`_
* `Grupo Troiano <http://grupotroiano.com.br>`_
* `Troiano <http://troiano.com.br>`_
* `Brands and Values <http://brandsandvalues.com.br>`_
* `Brigh Thouse <http://brighthouse.com.br>`_
* `Brand Insights <http://brandinsights.com.br>`_
