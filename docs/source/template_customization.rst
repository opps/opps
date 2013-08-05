Template Customization
======================

Opps default
------------

* Channel: templates/containers/list.html
* Content: templates/containers/detail.html


Custom
------

* templates/containers/<channel-name>/list.html
* templates/containers/<channel-name>/detail.html
* templates/containers/<channel-name>/<sub-channel-name>/list.html
* templates/containers/<channel-name>/<sub-channel-name>/detail.html


Channel conf
------------

All channel configuration is one json file, a channel can have more than one layout, changed when editing channel (file name **templates/containers/<channel-name>/channel.json**):

.. code-block:: json

    {"layout": ["home_1", "home_2"]}
