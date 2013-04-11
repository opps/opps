Opps CMS Example
================

## First things first

Create a virtualenv environment ( if you don't know what this is read
[this]("http://virtualenvwrapper.readthedocs.org/en/latest/")).

After the virtual environment creation you should do:

    $ pip install opps

Trouble installing Opps? Go
[here]("http://www.oppsproject.org/en/latest/installation.html")


## Create a project

    $ django-admin.py createproject mysite

Since the Opps CMS is modularized with several apps, we need to add the
base apps in the INSTALLED_APPS tuple: 

    INSTALLED_APPS (
		...
		'opps.core',
        'opps.articles',
        'opps.channels',
        'opps.images',
        'opps.search',
        'opps.sitemaps',
        'opps.sources',
    )

Now you can run:

	$ python manage.py syncdb
	$ python manage.py migrate


If you are having trouble to configure your project settings.py you can
look at our settings.py example.

And that's it! Don't forget to enable Django's admin to start adding
content!

Got any issues? Go to the [Opps Github
Issues]('http://github.com/opps/opps/issues')





