Git Tips
========

While some of this information repeats documentation that is already available on `GitHub Help`_, we thought it might be useful to collect and publish some of the most relevant information.


Forking Opps
------------

Assuming you have already `set up Git`_, the first step is to navigate to the `Opps project`_ page and select the Fork button at top-right.

Next, clone your fork (replace GH-USER with your GitHub username):

::

    git clone https://github.com/GH-USER/pelican.git

This adds a "remote" for your fork called "origin". Add the canonical Opps project as an additional remote called "upstream":

::

    cd opps
    git remote add upstream https://github.com/opps/opps.git


.. _`GitHub Help`: https://help.github.com/
.. _`set up Git`: https://help.github.com/articles/set-up-git
.. _`Opps project`: https://github.com/opps/opps
