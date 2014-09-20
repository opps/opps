#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.forms import widgets
from django.db.models import Field

from django.utils.safestring import mark_safe
from django.conf import settings


"""
To use ALOHA  configure in settings.py

OPPS_EDITOR = {
    'editor': 'aloha',
    'js': ("//cdn.aloha-editor.org/latest/lib/require.js",),
    "css": ("//cdn.aloha-editor.org/latest/css/aloha.css",)
}

To use redactor install redactor
pip install django-wysiwyg-redactor
or set your own static paths
OPPS_EDITOR = {
    'editor': 'redactor',
    'js': ('redactor/redactor.min.js',),
    "css": ('redactor/css/redactor.css',
               'redactor/css/django_admin.css')
}
"""

CONFIG = {
    'editor': 'tinymce',
    'js': ('/static/tinymce/tinymce.min.js',)
}

USER_CONFIG = getattr(settings, 'OPPS_EDITOR', {})

CONFIG.update(USER_CONFIG)

INIT_JS = {
    'tinymce': """
             <script src='/static/opps_tinymce.js'></script>
             <script src='/static/admin/opps/images/js/oppsfilebrowser.js'>
            </script>
              <script type="text/javascript">
            django.jQuery(document).ready(function(){
            tinymce.init(%s);
            });
              </script>""",

    'redactor': """<script type="text/javascript">
                  django.jQuery(document).ready(function(){
                      $("#%s").redactor(%s);
                  });
                  </script>""",

    'aloha': """<script type="text/javascript">
                     Aloha.ready( function() {
                        var $ = Aloha.jQuery;
                        $('#%s').aloha(%s);
                     });
                </script>"""
}


class OppsEditor(widgets.Textarea):

    class Media:
        js = CONFIG.get('js')
        css = {
            'all': CONFIG.get('css', [])
        }

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        self.custom_options = kwargs.pop('editor_options', {})
        self.allow_file_upload = kwargs.pop('allow_file_upload', True)
        self.allow_image_upload = kwargs.pop('allow_image_upload', True)
        super(OppsEditor, self).__init__(*args, **kwargs)

    def get_options(self, **kwargs):
        options = CONFIG.copy()
        for key in ('editor', 'css', 'js'):
            options.pop(key, None)
        options.update(kwargs)
        return json.dumps(options)

    def render(self, name, value, attrs=None):
        html = super(OppsEditor, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')

        editor = CONFIG.get('editor')

        if editor in ('tinymce',):
            options = self.get_options(selector="#{0}".format(id_))
            html += INIT_JS.get(CONFIG.get('editor')) % options
            html = html.replace('"CustomFileBrowser"', "CustomFileBrowser")
            html = html.replace("---editorid---", id_)
        else:
            if editor in ('aloha',):
                html += """
                <script
                src="http://cdn.aloha-editor.org/latest/lib/aloha.js"
                data-aloha-plugins="common/ui,
                                    common/format,
                                    common/list,
                                    common/link,
                                    common/highlighteditables">
                </script>
                """
            html += INIT_JS.get(editor) % (id_, self.get_options())

        return mark_safe(html)


class OppsEditorField(Field):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop('editor_options', {})
        upload_to = kwargs.pop('upload_to', '')
        allow_file_upload = kwargs.pop('allow_file_upload', True)
        allow_image_upload = kwargs.pop('allow_image_upload', True)
        self.widget = OppsEditor(
            editor_options=options,
            upload_to=upload_to,
            allow_file_upload=allow_file_upload,
            allow_image_upload=allow_image_upload
        )
        super(OppsEditorField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget}
        defaults.update(kwargs)
        return super(OppsEditorField, self).formfield(**defaults)


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^opps\.core\.widgets\.OppsEditorField"])
