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


Making your changes
-------------------

Create and switch to a new branch to house your feature or bugfix (replace `newfeaturebranch` with an appropriate name):

::

    git fetch upstream
    git checkout -b newfeaturebranch upstream/master

Once you are satisfied with your changes, run the tests and check coding standards:

::

    make test

Once the tests all pass and you are comfortable that your code complies with the suggested coding standards, add and commit your changes:

::

    git add changedfile1 changedfile2
    git commit

Push your new branch, and the commit(s) within, to your fork:

::

    git push origin newfeaturebranch


.. _`GitHub Help`: https://help.github.com/
.. _`set up Git`: https://help.github.com/articles/set-up-git
.. _`Opps project`: https://github.com/opps/opps
