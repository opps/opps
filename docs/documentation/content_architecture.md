The Content Archicteture
====================

![Opps Archicterure Details](https://raw.githubusercontent.com/opps/opps/master/docs/_static/opps_full_architecture.png)


The ``Container`` Model
====================

The content architecture starts with the Container Model. The Container is the basic model for everything in Opps.
And it is important that most objects used in frontend should extend Container.

When querying for overall objects it will query for ``Containers.Container`` in this case if you don't extend it, your object 
might stay out of the list, making you create a query only for it(redundant), instead of querying Containers.Container with a 
filter using your specific child_class.

The conventions of a Opps site is the model ``opps.containers.models.Container``. Each ``container``
instance is stored in a hierarchical tree to form the content navigation, and an interface for
managing the structure of the navigation tree is provided in the admin via ``opps.containers.admin.ContainerAdmin``.


Creating Custom Content Type
----------------------------

In order to handle different content type that require more structured content than provided by
the ``Post``, ``Album`` or ``Link`` model, you can simply create your own models that inherit 
from ``Container``. For example if we wanted to have content that were **music**, **author** and **studio**:


```python
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
    from django.contrib import admin
    from opps.containers.admin import ContainerAdmin
    from .models import Musics

    admin.site.register(Musics, ContainerAdmin)
```

ContainerBox
-------------

Probably the most accessed class in the dashboard.
With ContainerBox you can group Containers to be fetched in the front.
You can fetch manually by picking containers in the inlines or you can use [QuerySet](https://github.com/opps/opps/tree/master/opps/boxes) to fetch automaticaly.
They do not affect each other, it will depend on the front to choose between who to render, automatic or manual.
Normally the best way to go is by giving priority to manual inputs(Inlines) and when those are missing/empty then you render the Queryset results in it's place.

Content Group
--------------

The ContainerBox.content_group attribute is used to give context and the ability to query for unique items(excluding repetitions).
So you can fragment your page into N ContainerBoxes and make all of them use querysets from the same place and they won't repeat content as long as they share the same Content Group.

Methods
--------

Two methods are widely used here:

 - ContainerBox.ordered_box_containers (Will fetch containers from the Inlines ordered by it's order field)
 - ContainerBox.get_queryset (Will fetch the containers from the Queryset associated on the ContainerBox)

One important thing is that he returns the Inline element, not the container itself, since the Inline have fields that might override the original container fields. *To get the original container* associated you must access the ".container" property like bellow:

    {% set containerbox.ordered_box_containers as items %}
    {{items.0}} {# this is a Inline element #}
    {{items.0.container}} {# this is the container held by the inline element #}

ContainerBoxContainers (Inline)
--------------------------------

It is a row like structure where you can bind containers inside it to form a group inside a ContainerBox.
When binding a container and saving, it will load the matching fields content into the ContainerBoxContainer.
It is important to have the same container displayed a little differently on many locations.

Mirror
------

It is a workaround for many-2-many relations between Containers.Container and Channels.
Creates clones of the Container object to be associated in other channels and is updated by a Celery task.
*Should be obsolete in Opps 0.3*


The ``Channel`` Model
====================

Channel objects are used like categories and/or sections in Opps.
They group content and give flexibility in templating.

Personalizing a Channel
------------------------

To extend a Channel template as channel is a container you must have a folder structure like the following:

    .../templates/containers/<channel-slug>/template-name.html
    .../templates/containers/<channel-slug>/<sub-channel-slug>/template-name.html

To personalize any channel template you must understand how template
hierarchy works.
Let's suppose the folowing structure:

  - /
    - news/
      - cars/
      - economy/
         - country/
         - international/

From this point, the templates that target *All* the hypothetical channels are:

    /containers/list.html
    /containers/detail.html

In case I want to specify a template only for */news/cars*:

	  # Symbolic functions
    mkdir /containers/news/cars
    vim /containers/news/cars/list.html
    vim /containers/news/cars/detail.html

Now only for */news*:

    mkdir /containers/news
    vim /containers/news/list.html
    vim /containers/news/detail.html

Some more examples for:

#### Channel: 

templates/containers/list.html

#### Content: 

templates/containers/detail.html

    containers/<channel-slug>/<sub-channel-slug>/<container-slug>/detail.html
    containers/<channel-slug}/<sub-channel-slug>/<container-child-class>_detail.html
    containers/<channel-slug>/<sub-channel-slug>/detail.html
    containers/<channel-slug>/<container-child-class>_detail.html
    containers/channel/detail.html
    containers/detail.html

**BUT** when we create a template for */news* **All** channels below will now consider this template.
The only channel not affected by this template is */news/cars* whose has it's own template structure.
It won't be affected.

Theming the Channel
-------------------

Channels have a special options called *Layout* this option let you choose a template type for this channel, which is mapped to a html.
This option is manually controlled by a file named **channel.json**.

This file is hierarquically loaded like templates, and allows to create new template names which can be switched in the channel dashboard.

A example of this file could be /containers/channel.json:

    {"layout": ["my_template"]}

If you choose this option in the dashboard it will look for this template:

    .../templates/containers/my_template.html

This way you can prepare special templates for holidays and other temporary changes.

The ``Article`` Model
====================

Post
----

Not only a simple Post but you can bind separately:

 - Album
 - Container

When rendering Album inside a Post there is a simple rule for the image order:

  1. Post main image
  2. Album main image
  3. Album binded images

Album
------

Group of Image objects can be binded on other Containers or rendered by itself.

Link
-----
Representation of external links(normally) but can point to internal objects(Container).
This behavior is controlled by the flag **is_local**.

------------------------

##### Representation
![Opps Content Details](https://raw.githubusercontent.com/opps/opps/master/docs/_static/opps_content_archicteture.png)


QuerySet
====================

The Queryset feature is inside in the ``Box`` Model, is used to gatter automatic data.
It is used together(but not uniquely) with [Containerbox](https://github.com/opps/opps/tree/master/opps/containers) this way we can make the box 
update by itself based on some params:

 - Model (Which model to get, for example ``Containers.Container`` or ``Post``)
 - ``Channel`` (Specific channel to grab data from)
 - Recursive (Look into this channels childs(subchannels) recursivelly)
 - Filters (Json filters based on [django query language](https://docs.djangoproject.com/en/dev/topics/db/queries/#retrieving-specific-objects-with-filters) will be passed to .filters(**kwargs))
 - Excludes (same as filters but will be passed to .excludes(**kwargs) check the [docs](https://docs.djangoproject.com/en/dev/topics/db/queries/#retrieving-specific-objects-with-filters))
 - Order (Passed to order_by as DESC(-) and ASC(+) if no order_field is passed, it will order by ID)
 - Limit and Offset (Use like you would use python slice [offset:limit])
