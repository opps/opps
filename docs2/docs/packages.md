## Packages

### opps.api

##### Get all containers object

* /api/v1/container/?format=json


##### Get container object

* /api/v1/{child class}/{id}/?format=json
* /api/v1/post/{id}/?format=json
* /api/v1/album/{id}/?format=json
* /api/v1/link/{id}/?format=json

---------------------

### opps.archives

### opps.articles

##### Post

Not only a simple Post but you can bind separately:

 - Album
 - Container

When rendering Album inside a Post there is a simple rule for the image order:

  1. Post main image
  2. Album main image
  3. Album binded images

##### Album

Group of Image objects can be binded on other Containers or rendered by itself.

##### Link

Representation of external links(normally) but can point to internal objects(Container).
This behavior is controlled by the flag **is_local**.

---------------------

### opps.boxes

##### QuerySet

Queryset is used to gatter automatic data.
It is used together(but not uniquely) with [Containerbox](https://github.com/opps/opps/tree/master/opps/containers) this way we can make the box update by itself based on some params:

 - Model (Which model to get, for example [Containers.Container](https://github.com/opps/opps/tree/master/opps/containers#container) or Post)
 - [Channel](https://github.com/opps/opps/tree/master/opps/channels#channel) (Specific channel to grab data from)
 - Recursive (Look into this channels childs(subchannels) recursivelly)
 - Filters (Json filters based on [django query language](https://docs.djangoproject.com/en/dev/topics/db/queries/#retrieving-specific-objects-with-filters) will be passed to .filters(**kwargs))
 - Excludes (same as filters but will be passed to .excludes(**kwargs) check the [docs](https://docs.djangoproject.com/en/dev/topics/db/queries/#retrieving-specific-objects-with-filters))
 - Order (Passed to order_by as DESC(-) and ASC(+) if no order_field is passed, it will order by ID)
 - Limit and Offset (Use like you would use python slice [offset:limit])

 More about using it on [Containerbox](https://github.com/opps/opps/tree/master/opps/containers)

---------------

### opps.channels

Channel objects are used like categories and/or sections in Opps.
They group content and give flexibility in templating.

##### Personalizing a Channel

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

**BUT** when we create a template for */news* **All** channels below will now consider this template.
The only channel not affected by this template is */news/cars* whose has it's own template structure.
It won't be affected.

##### Theming the Channel

Channels have a special options called *Layout* this option let you choose a template type for this channel, which is mapped to a html.
This option is manually controlled by a file named **channel.json**.

This file is hierarquically loaded like templates, and allows to create new template names which can be switched in the channel dashboard.

A example of this file could be /containers/channel.json:

    {"layout": ["my_template"]}

If you choose this option in the dashboard it will look for this template:

    .../templates/containers/my_template.html

This way you can prepare special templates for holidays and other temporary changes.

----------------

### opps.containers

Container is the basic model for everything in Opps.
And it is important that most objects used in frontend should extend Container.

When querying for overall objects it will query for Containers.Container in this case if you do not extend it, your object might stay out of the list, making you create a query only for it(redundant), instead of querying Containers.Container with a filter using your specific child_class.

##### ContainerBox

Probably the most accessed class in the dashboard.
With ContainerBox you can group Containers to be fetched in the front.
You can fetch manually by picking containers in the inlines or you can use [QuerySet](https://github.com/opps/opps/tree/master/opps/boxes) to fetch automaticaly.
They do not affect each other, it will depend on the front to choose between who to render, automatic or manual.
Normally the best way to go is by giving priority to manual inputs(Inlines) and when those are missing/empty then you render the Queryset results in it's place.

##### Content Group

The ContainerBox.content_group attribute is used to give context and the ability to query for unique items(excluding repetitions).
So you can fragment your page into N ContainerBoxes and make all of them use querysets from the same place and they won't repeat content as long as they share the same Content Group.

##### Methods

Two methods are widely used here:

 - ContainerBox.ordered_box_containers (Will fetch containers from the Inlines ordered by it's order field)
 - ContainerBox.get_queryset (Will fetch the containers from the Queryset associated on the ContainerBox)

One important thing is that he returns the Inline element, not the container itself, since the Inline have fields that might override the original container fields. *To get the original container* associated you must access the ".container" property like bellow:

    {% set containerbox.ordered_box_containers as items %}
    {{items.0}} {# this is a Inline element #}
    {{items.0.container}} {# this is the container held by the inline element #}

##### ContainerBoxContainers (Inline)

It is a row like structure where you can bind containers inside it to form a group inside a ContainerBox.
When binding a container and saving, it will load the matching fields content into the ContainerBoxContainer.
It is important to have the same container displayed a little differently on many locations.

##### Mirror

It is a workaround for many-2-many relations between Containers.Container and Channels.
Creates clones of the Container object to be associated in other channels and is updated by a Celery task.
*Should be obsolete in Opps 0.3*

--------------

### opps.contrib
#### opps.contrib.admin

Referenced in code as *ADMIN_SHORTCUTS* on settings.py.
It is a non-dynamic way of choosing which module will be available in the top menu.

Simple dict with the following structure:

    'shortcuts': [
        {
            'url': '/<url>/', # url of the top option or root node
            'title': '<title>', # title of the root node
            'class': '<class_names>', # class to be added to html class attribute
            'open_new_window': True, # should open in new window or not
            'children': [ 
                'url_name': 'admin:<moule_name>_<class_name>_changelist', # pointer to module admin url(check the real example below)
                'title': '<title>', # option title
                'include_add_link': True, # if should or not include the add option
                'help': '<help_text>', # help text when hovering
                'app_permission': (<module_name>, <class_name>)
            ],
            'can_change': True, # Used only when not a module so can't check for user permission (more like visible or not to the user)
        },
        ...
    ]

Real examplewith static options and generated ones:

    ADMIN_SHORTCUTS = [
    {
        'shortcuts': [
            {
                'url': '/admin/',
                'title': 'Home'
            },
            {
                'url': '#',
                'title': 'Conteúdo',
                'class': 'file2',
                'children': [
                    {
                        'url_name': 'admin:%s_changelist' % item[0],
                        'title': item[1],
                        'include_add_link': True,
                        'help': 'Listar %s' % item[1],
                        'app_permission': (item[0].split('_')[0], item[0].split('_')[1])
                    } for item in (
                        ('channels_channel', 'Channels'),
                        ('articles_post', 'Posts'),
                        ('articles_album', 'Albums'),
                        ('articles_link', 'Links'),
                        ('flatpages_flatpage', 'Flatpages'),
                        ('polls_poll', 'Polls'),
                        ('tags_tag', 'Tags'),
                        ('encurtador_shortener', 'Shorteners')
                    )
                ] + [
                     {'url': '/admin/feedcrawler/entry/', 'title': 'News Crawler',
                     'app_permission': ('feedcrawler', 'entry')}
                ]
            },

            {
                'url': '#',
                'title': 'Multimedia',
                'class': 'file2',
                'children': [
                    {
                        'url_name': 'admin:%s_changelist' % item[0],
                        'title': item[1],
                        'help': 'Listar %s' % item[1],
                        'app_permission': (item[0].split('_')[0], item[0].split('_')[1])
                    } for item in (
                        ('images_image', 'Images'),
                        ('multimedias_video', 'Videos'),
                        ('multimedias_audio', 'Audios'),
                        ('hubcasts_streaming', 'Streamings')
                    )
                ]
            },

            {
                'url': '/',
                'title': 'See Website',
                'open_new_window': True,
                'help': 'Click to check your website',
                'can_change': True,
                'children': []
            }
        ]
    }]

As you can see we have a loop for the module dict-objects and a static option example.

Static option

    {
        'url': '/',
        'title': 'See Website',
        'open_new_window': True,
        'help': 'Click to check your website',
        'can_change': True,
        'children': []
    }

In this case as it is not a module you need **can_change** flag to make it appear.

Module option

    {
        'url':'/admin/feedcrawler/entry/',
        'title': 'News Crawler',
        'app_permission': ('feedcrawler', 'entry')
    }

This options will be based on feedcrawler.entry object data.

And the dynamic(loop) approach, can be changed if necessary or even create a module to replace this logic

    {
        'url': '#',
        'title': 'Multimedia',
        'class': 'file2',
        'children': [
            {
                'url_name': 'admin:%s_changelist' % item[0],
                'title': item[1],
                'help': 'Listar %s' % item[1],
                'app_permission': (item[0].split('_')[0], item[0].split('_')[1])
            } for item in (
                ('images_image', 'Images'),
                ('multimedias_video', 'Videos'),
                ('multimedias_audio', 'Audios'),
                ('hubcasts_streaming', 'Streamings')
            )
        ]
    }

This way you just have to list your modules and they will be rendered under the group name in this case "Multimedia".

---------------

#### opps.contrib.feeds

#### opps.contrib.fileupload

#### opps.contrib.logging

Application to generate log project actions

###### Example


    $.ajax({
        type: 'POST',
        url: '/api/v1/contrib/logging/',
        data: '{"application": "player", "action": "play"}',
        dataType: "application/json",
        processData:  false,
        contentType: "application/json"
    });



#### opps.contrib.mobile

#### opps.contrib.multisite

#### opps.contrib.notifications

### opps.core
#### opps.core.cache

Cache in Opps is very simple.
It uses *django.core.cache* and the current pattern to use it is to define a unique **cachekey** based on context and store objects or rendered response in it.

##### Caching on Templatetags

Example of storing:

    from django.core.cache import cache
    cachekey = "ContainerBox-{}-{}-{}-{}".format(
    	slug,
    	template_name,
    	is_mobile,
    	current_site.id)

    # now we can test if there is something here to render:

    render = cache.get(cachekey)
    if render:
    	return render

    # else we do our business and save in this cachekey

    ...

	render = our_rendered_content
    cache.set(cachekey, render, settings.OPPS_CACHE_EXPIRE)
    return render

To store objects is the same proccess instead of html, you can pass the object list to cache.set and it will work fine.
This method could be used on views too.

##### Caching Routes

Caching entire routes is very simple there is a method for that:

    from opps.core.cache import cache_page
    
    (r'^route_pattern$', cache_page(<seconds>)(<page_content>)),

	# real example

	url(r'^(rss|feed)$', cache_page(settings.OPPS_CACHE_EXPIRE)(
        ContainerFeed()), name='feed')

##### Caching Views

Caching views are as simples as adding the following decorator above your view function:

	from opps.core.cache import cache_page

    @cache_page(<seconds>)
    def my_view_function():
    	...

##### Caching inside templates

On front you can use cache methods to cache a single fragment of the page like a menu, list or anything that might break your application.

	{% load cache %}
    {% cache <seconds> <cache_identifier> <params> %}
    	...<your content>...
    {% endcache %}

    # real example
	{% cache 3600 menu %}
		...menu here...
	{% endcache %}

You can find much more information about caching on [django docs here](https://docs.djangoproject.com/en/dev/topics/cache/)

---------------    

#### opps.core.tags

#### opps.core.templatetags

### opps.db

#### opps.db._redis

#### opps.db.backends.postgresql_psycopg2

### opps.fields

### opps.flatpages

### opps.images

### opps.search

### opps.sitemaps

### opps.views

## Opps Apps

* [opps.polls](https://github.com/opps/opps-polls)
* [opps.infographics](https://github.com/opps/opps-infographics)
* [opps.ganalytics](https://github.com/opps/opps-ganalytics)
* [opps.promos](https://github.com/opps/opps-promos)
* [opps.timelinejs](https://github.com/opps/opps-timelinejs)
* [opps.registration](https://github.com/opps/opps-registration)
* [more...](https://github.com/opps)
