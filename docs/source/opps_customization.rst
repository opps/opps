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


Set your own static paths:


.. code-block:: python

    OPPS_EDITOR = {
        'editor': 'redactor',
        'js': ('redactor/redactor.min.js',),
        "css": ('redactor/css/redactor.css',
                'redactor/css/django_admin.css')
    }
