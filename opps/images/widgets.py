from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from opps.channels.models import Channel


class MultipleUpload(forms.FileInput):
    def render(self, name, value, attrs=None):
        _value = ""
        if value:
            _value = "{}{}".format(settings.MEDIA_URL, value)
        return render_to_string("admin/opps/images/multiupload.html",
                                {"name": name, "value": _value,
                                 "STATIC_URL": settings.STATIC_URL})


class CropExample(forms.TextInput):
    def render(self, name, value, attrs=None):
        return render_to_string(
            "admin/opps/images/cropexample.html",
            {"name": name, "value": value,
             'STATIC_URL': settings.STATIC_URL,
             "THUMBOR_SERVER": settings.THUMBOR_SERVER,
             "THUMBOR_MEDIA_URL": settings.THUMBOR_MEDIA_URL})


class ArticleGenerator(forms.TextInput):
    def render(self, name, value, attrs=None):
        channels = Channel.objects.filter(published=True)
        return render_to_string(
            "admin/opps/images/articlegenerator.html",
            {"name": name, "value": value,
             'STATIC_URL': settings.STATIC_URL,
             'channels': channels})
