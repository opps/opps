
Channel
=======

Channel objects are used like categories and/or sections in Opps.
They group content and give flexibility in templating.

Personalizing a Channel
-----------------------

To extend a Channel template as channel is a container you must have a folder structure like the following:

    .../templates/containers/<channel-slug>/template-name.html
    .../templates/containers/<channel-slug>/<sub-channel-slug>/template-name.html

To personalize any channel template you must understand how template
hierarchy works.
Let's suppose the folowing structure:

  - /
    - news/
      - cars/
      - economy/
         - country/
         - international/

From this point, the templates that target *All* the hypothetical channels are:

    /containers/list.html
    /containers/detail.html

In case I want to specify a template only for */news/cars*:

	  # Symbolic functions
    mkdir /containers/news/cars
    vim /containers/news/cars/list.html
    vim /containers/news/cars/detail.html

Now only for */news*:

    mkdir /containers/news
    vim /containers/news/list.html
    vim /containers/news/detail.html

**BUT** when we create a template for */news* **All** channels below will now consider this template.
The only channel not affected by this template is */news/cars* whose has it's own template structure.
It won't be affected.

Theming the Channel
-------------------

Channels have a special options called *Layout* this option let you choose a template type for this channel, which is mapped to a html.
This option is manually controlled by a file named **channel.json**.

This file is hierarquically loaded like templates, and allows to create new template names which can be switched in the channel dashboard.

A example of this file could be /containers/channel.json:

    {"layout": ["my_template"]}

If you choose this option in the dashboard it will look for this template:

    .../templates/containers/my_template.html

This way you can prepare special templates for holidays and other temporary changes.
