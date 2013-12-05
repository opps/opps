"""
Wrapper for loading templates from the filesystem based on the HTTP
request.

This template loader will use the thread-local value of
``template_dirs`` defined by the middlewares at
``opps.contrib.mobile.middleware`` to determine which template
directory to use.

"""

from django.conf import settings
from django.template.base import TemplateDoesNotExist
from django.template.loaders.filesystem import Loader as FileSystemLoader
from django.utils._os import safe_join

from opps.contrib.mobile.middleware import THREAD_LOCALS


class Loader(FileSystemLoader):

    def get_template_sources(self, template_name, template_dirs=None):
        if not template_dirs:
            template_dirs = getattr(
                THREAD_LOCALS,
                'template_dirs',
                settings.TEMPLATE_DIRS
            )
        for template_dir in template_dirs:
            try:
                yield safe_join(template_dir, template_name)
            except UnicodeDecodeError:
                # The template dir name was a bytestring that wasn't
                # valid UTF-8.
                raise
            except ValueError:
                # The joined path was located outside of this particular
                # template_dir (it might be inside another one, so this isn't
                # fatal).
                pass
