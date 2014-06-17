# Template Customization

Opps default
------------

* Channel: templates/containers/list.html
* Content: templates/containers/detail.html


Details
-------

* containers/{channel-slug}/{sub-channel-slug}/{container-slug}/detail.html
* containers/{channel-slug}/{sub-channel-slug}/{container-child-class}_detail.html
* containers/{channel-slug}/{sub-channel-slug}/detail.html
* containers/{channel-slug}/{container-child-class}_detail.html
* containers/channel/detail.html
* containers/detail.html


Channel conf
------------

All channel configuration is one json file, a channel can have more than one layout, changed when editing channel 
(file name **templates/containers/{channel-name}/channel.json**):


    {"layout": ["home_1", "home_2"]}

    
# Opps Customization

Opps Editor
-----------

By default it uses `Tinymce <http://www.tinymce.com/>`_

To use aloha
************

    OPPS_EDITOR = {
        'editor': 'aloha',
        'js': ("//cdn.aloha-editor.org/latest/lib/require.js",),
        "css": ("//cdn.aloha-editor.org/latest/css/aloha.css",)
    }


To use redactor
***************

Install redactor:

    pip install django-wysiwyg-redactor

Add django redactor to your INSTALLED_APPS:

    INSTALLED_APPS += ('redactor')

Add django redactor to your urls.py:

    
    urlpatterns = patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^', include('opps.urls')),
        # django redactor
        url(r'^redactor/', include('redactor.urls')),
    )

Set your own static paths:


    OPPS_EDITOR = {
        'editor': 'redactor',
        'js': ('redactor/redactor.min.js',),
        "css": ('redactor/css/redactor.css',
                'redactor/css/django_admin.css')
    }


