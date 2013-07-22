Opps Customization
==================

Opps Editor
-----------

By default it uses `Tinymce <http://www.tinymce.com/>`_

To use aloha
************

.. code-block:: python

    OPPS_EDITOR = {
        'editor': 'aloha',
        'js': ("//cdn.aloha-editor.org/latest/lib/require.js",),
        "css": ("//cdn.aloha-editor.org/latest/css/aloha.css",)
    }


To use redactor
***************

Install redactor:

.. code-block:: bash

    pip install django-wysiwyg-redactor

Add django redactor to your INSTALLED_APPS:

.. code-block:: python
    INSTALLED_APPS += ('redactor')

Add django redactor to your urls.py:

.. code-block:: python
    
    urlpatterns = patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^', include('opps.urls')),
        # django redactor
        url(r'^redactor/', include('redactor.urls')),
    )

Set your own static paths:

.. code-block:: python

    OPPS_EDITOR = {
        'editor': 'redactor',
        'js': ('redactor/redactor.min.js',),
        "css": ('redactor/css/redactor.css',
                'redactor/css/django_admin.css')
    }
