from django import forms
from django.conf import settings
from django.template.loader import render_to_string


class MultipleUpload(forms.FileInput):
    def render(self, name, value, attrs=None):
        value = ""
        if value:
            _value = "{0}{1}".format(settings.MEDIA_URL, value)
        return render_to_string(
            "admin/opps/images/multiupload.html",
            {"name": name, "value": _value, "STATIC_URL": settings.STATIC_URL}
        )


class CropExample(forms.TextInput):
    def render(self, name, value, attrs=None):
        return render_to_string(
            "admin/opps/images/cropexample.html",
            {
                "name": name, "value": value,
                'STATIC_URL': settings.STATIC_URL,
                "THUMBOR_SERVER": settings.THUMBOR_SERVER,
                "THUMBOR_MEDIA_URL": settings.THUMBOR_MEDIA_URL,
                "THUMBOR_ENABLED": settings.THUMBOR_ENABLED
            }
        )
