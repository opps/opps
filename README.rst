Opps - OPen Publishing System
=============================
.. |Opps| image:: docs/source/_static/opps.jpg
    :alt: Opps Open Source Content Management

An *Open Source Content Management* for the **magazine** websites and **high-traffic**, using the Django Framework.

.. image:: https://drone.io/github.com/opps/opps/status.png
    :target: https://drone.io/github.com/opps/opps/latest)
    :alt: Build Status - Drone

.. image:: https://travis-ci.org/opps/opps.png?branch=master
    :target: https://travis-ci.org/opps/opps
    :alt: Build Status - Travis CI

.. image:: https://pypip.in/v/opps/badge.png
    :target: https://crate.io/packages/opps/
    :alt: Pypi version

.. image:: https://pypip.in/d/opps/badge.png
    :target: https://crate.io/packages/opps/
    :alt: Pypi downloads


Contacts
========

The place to create issues is `opps's github issues <https://github.com/opps/opps/issues>`_. The more information you send about an issue, the greater the chance it will get fixed fast.

If you are not sure about something, have a doubt or feedback, or just want to ask for a feature, feel free to join `our mailing list <http://groups.google.com/group/opps-developers>`_, or, if you're on FreeNode (IRC), you can join the chat `#opps <http://webchat.freenode.net/?channels=opps>`_.


Run example
===========

.. code-block:: bash

    git clone git@github.com:opps/opps.git
    cd opps
    python setup.py develop
    opps-admin.py startproject PROJECT_NAME
    cd PROJECT_NAME
    python manage.py syncdb
    python manage.py migrate
    python manage.py collectstatic
    python manage.py runserver


Sponsor
=======

* `YACOWS <http://yacows.com.br/>`_


License
=======

Copyright 2013 *Opps* Project and other contributors.

Licensed under the `MIT License <http://opensource.org/licenses/MIT>`_