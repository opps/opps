Template Customization
======================

Opps default
------------

* Channel: templates/containers/list.html
* Content: templates/containers/detail.html


Details
-------

* containers/<channel-slug>/<sub-channel-slug>/<container-slug>/detail.html
* containers/<channel-slug>/<sub-channel-slug>/<container-child-class>_detail.html
* containers/<channel-slug>/<sub-channel-slug>/detail.html
* containers/<channel-slug>/<container-child-class>_detail.html
* containers/<channel>/detail.html
* containers/detail.html


Channel conf
------------

All channel configuration is one json file, a channel can have more than one layout, changed when editing channel (file name **templates/containers/<channel-name>/channel.json**):

.. code-block:: json

    {"layout": ["home_1", "home_2"]}
