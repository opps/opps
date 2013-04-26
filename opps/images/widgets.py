from django import forms
from django.conf import settings
from django.template.loader import render_to_string


class MultipleUpload(forms.FileInput):

    def render(self, name, value, attrs=None):
        _value = ""
        if value:
            _value = "{0}{1}".format(settings.MEDIA_URL, value)
        return render_to_string("admin/opps/images/multiupload.html",
                                {"name": name, "value": _value,
                                 "STATIC_URL": settings.STATIC_URL})
