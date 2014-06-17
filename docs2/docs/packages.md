# Packages

opps.api
--------

Get all containers object
-------------------------

* /api/v1/container/?format=json


Get container object
--------------------

* /api/v1/<child class>/<id>/?format=json
* /api/v1/post/<id>/?format=json
* /api/v1/album/<id>/?format=json
* /api/v1/link/<id>/?format=json

opps.archives
-------------

opps.articles
-------------

opps.boxes
----------

opps.channels
-------------

opps.containers
---------------

opps.contrib.feeds
------------------

opps.contrib.fileupload
-----------------------

opps.contrib.logging
--------------------

Application to generate log project actions

Example
*******


    $.ajax({
        type: 'POST',
        url: '/api/v1/contrib/logging/',
        data: '{"application": "player", "action": "play"}',
        dataType: "application/json",
        processData:  false,
        contentType: "application/json"
    });



opps.contrib.mobile
-------------------

opps.contrib.multisite
----------------------

opps.contrib.notifications
--------------------------

opps.core.tags
--------------

opps.core.templatetags
----------------------

opps.db._redis
--------------

opps.db.backends.postgresql_psycopg2
------------------------------------

opps.fields
-----------

opps.flatpages
--------------

opps.images
-----------

opps.search
-----------

opps.sitemaps
-------------

opps.views
----------

# Opps Apps

* [opps.polls](https://github.com/opps/opps-polls)
* [opps.infographics](https://github.com/opps/opps-infographics)
* [opps.ganalytics](https://github.com/opps/opps-ganalytics)
* [opps.promos](https://github.com/opps/opps-promos)
* [opps.timelinejs](https://github.com/opps/opps-timelinejs)
* [opps.registration](https://github.com/opps/opps-registration)
* [more...](https://github.com/opps)
