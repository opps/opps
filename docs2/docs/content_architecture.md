ontent Architecture
====================

The ``Container`` Model
-----------------------

The conventions of a Opps site is the model ``opps.containers.models.Container``. Each ``container``
instance is stored in a hierarchical tree to form the content navigation, and an interface for
managing the structure of the navigation tree is provided in the admin via ``opps.containers.admin.ContainerAdmin``.


Creating Custom Content Type
----------------------------

In order to handle different content type that require more structured content than provided by
the ``Post``, ``Album`` or ``Link`` model, you can simply create your own models that inherit 
from ``Container``. For example if we wanted to have content that were **music**, **author** and **studio**:


```python

    # -*- coding: utf-8 -*-
    from django.db import models
    from opps.containers.models import Container


    class Musics(Container):
        music = models.CharField(_(u"Music"), max_length=140)
        author = models.CharField(_(u"Author"), max_length=140)
        studio = models.CharField(_(u"Studio"), max_length=200)

        class META:
            verbose_name = _('Music')
            verbose_name_plural = _('Musics')
```

Next you’ll need to register your model with Django’s admin to make it available as a content type.
If your content type only exposes some new fields that you’d like to make editable in the admin, 
you can simply register your model using the ``opps.containers.admin.ContainerAdmin`` class:


```python

    # -*- coding: utf-8 -*-
    from django.contrib import admin
    from opps.containers.admin import ContainerAdmin
    from .models import Musics

    admin.site.register(Musics, ContainerAdmin)
```

