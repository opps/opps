
Container
=========

Container is the basic model for everything in Opps.
And it is important that most objects used in frontend should extend Container.

When querying for overall objects it will query for Containers.Container in this case if you do not extend it, your object might stay out of the list, making you create a query only for it(redundant), instead of querying Containers.Container with a filter using your specific child_class.

ContainerBox
============

Probably the most accessed class in the dashboard.
With ContainerBox you can group Containers to be fetched in the front.
You can fetch manually by picking containers in the inlines or you can use [QuerySet](https://github.com/opps/opps/tree/master/opps/boxes) to fetch automaticaly.
They do not affect each other, it will depend on the front to choose between who to render, automatic or manual.
Normally the best way to go is by giving priority to manual inputs(Inlines) and when those are missing/empty then you render the Queryset results in it's place.

Content Group
-------------

The ContainerBox.content_group attribute is used to give context and the ability to query for unique items(excluding repetitions).
So you can fragment your page into N ContainerBoxes and make all of them use querysets from the same place and they won't repeat content as long as they share the same Content Group.

Methods
-------

Two methods are widely used here:

 - ContainerBox.ordered_box_containers (Will fetch containers from the Inlines ordered by it's order field)
 - ContainerBox.get_queryset (Will fetch the containers from the Queryset associated on the ContainerBox)

One important thing is that he returns the Inline element, not the container itself, since the Inline have fields that might override the original container fields. *To get the original container* associated you must access the ".container" property like bellow:

    {% set containerbox.ordered_box_containers as items %}
    {{items.0}} {# this is a Inline element #}
    {{items.0.container}} {# this is the container held by the inline element #}

ContainerBoxContainers (Inline)
===============================

It is a row like structure where you can bind containers inside it to form a group inside a ContainerBox.
When binding a container and saving, it will load the matching fields content into the ContainerBoxContainer.
It is important to have the same container displayed a little differently on many locations.

Mirror
======

It is a workaround for many-2-many relations between Containers.Container and Channels.
Creates clones of the Container object to be associated in other channels and is updated by a Celery task.
*Should be obsolete in Opps 0.3*