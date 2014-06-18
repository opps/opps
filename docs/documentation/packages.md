# General Packages

opps.api
--------

Get all containers object

* /api/v1/container/?format=json


Get container object

* /api/v1/{child class}/{id}/?format=json
* /api/v1/post/{id}/?format=json
* /api/v1/album/{id}/?format=json
* /api/v1/link/{id}/?format=json

opps.archives
-------------


opps.contrib
------------
### opps.contrib.admin

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

### opps.contrib.feeds

### opps.contrib.fileupload

### opps.contrib.logging

Application to generate log project actions

Example


    $.ajax({
        type: 'POST',
        url: '/api/v1/contrib/logging/',
        data: '{"application": "player", "action": "play"}',
        dataType: "application/json",
        processData:  false,
        contentType: "application/json"
    });



### opps.contrib.mobile

### opps.contrib.multisite

### opps.contrib.notifications

opps.core
---------
### opps.core.cache

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

### opps.core.tags

### opps.core.templatetags

opps.db
-------

### opps.db._redis

### opps.db.backends.postgresql_psycopg2

opps.fields
-----------

opps.flatpages
--------------

opps.images
-----------

opps.search
------------

opps.sitemaps
-------------

opps.views
----------
