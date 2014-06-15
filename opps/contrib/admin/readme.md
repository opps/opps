
Admin Menu
==========

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