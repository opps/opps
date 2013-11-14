Packages
========

opps.api
--------

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

.. code-block:: javascript

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
