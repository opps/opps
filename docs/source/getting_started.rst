Getting Started
===============


Getting help
------------

Should you run into trouble and can’t figure out how to solve it yourself, you can get help from either our mailinglist or IRC channel #opps on the irc.freenode.net network.


Start
-----


.. code-block:: bash

    git clone https://github.com/opps/opps.git
    cd opps
    python setup.py develop
    opps-admin.py startproject PROJECT_NAME
    cd PROJECT_NAME
    python manage.py syncdb --noinput
    python manage.py migrate
    python manage.py collectstatic --noinput
    python manage.py runserver


Installation
------------

You can use pip to install Opps and requirements

.. code-block:: bash

    pip install opps

or

.. code-block:: bash

    git clone git@github.com:opps/opps.git
    cd opps
    python setup.py install


Start project
-------------

You can use `opps-admin.py` to start new project

.. code-block:: bash

    opps-admin.py startproject PROJECT_NAME

