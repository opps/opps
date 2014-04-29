Opps CMS Example
================

## First things first

Create a virtualenv environment ( if you don't know what this is read
[this](http://virtualenvwrapper.readthedocs.org/en/latest/)).

After the virtual environment creation you should do:

	$ pip install -r ../requirements.txt


### Run it!

	$ python manage.py syncdb
	$ python manage.py migrate

Now you can run:

	$ python manage.py runserver


Got any issues? Go to the [Opps Github
Issues](http://github.com/opps/opps/issues)
