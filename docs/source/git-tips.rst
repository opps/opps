Git Tips
========

While some of this information repeats documentation that is already available on `GitHub Help`_, we thought it might be useful to collect and publish some of the most relevant information.


Forking Opps
------------

Assuming you have already `set up Git`_, the first step is to navigate to the `Opps project`_ page and select the Fork button at top-right.

Next, clone your fork (replace GH-USER with your GitHub username):

::

    git clone https://github.com/GH-USER/opps.git

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


Issuing a pull request
----------------------

Read the `GitHub pull request documentation`_ first. Then navigate to your Opps fork at `https://github.com/GH-USER/opps`, select the new branch from the drop-down, and select "Pull Request". Enter a title and description for your pull request, review the proposed changes using the "Commits" and "Files Changed" tabs, and select "Send pull request".

If someone reviews your contribution and ask you to make more changes, do so and then rebase to upstream master:

::

    git checkout newfeaturebranch
    git fetch upstream
    git rebase -p upstream/master

When prompted, include a relevant commit message, describing all your changes. Finally, push your changes via:

::

    git push --force origin newfeaturebranch


Squashing commits
-----------------

If you are asked to squash your commits:

::

    git checkout newfeaturebranch
    git fetch upstream
    git rebase upstream/master
    git rebase -i


When prompted, mark your initial commit with pick, and all your follow-on commits with squash.

Then edit the commit message to make sense, taking out any extraneous information and succinctly describing your changes. Finally, push your changes via:

::

    git push --force origin newfeaturebranch


Relevant Resources
------------------

* `Git merge vs. rebase`_


.. _`GitHub Help`: https://help.github.com/
.. _`set up Git`: https://help.github.com/articles/set-up-git
.. _`Opps project`: https://github.com/opps/opps
.. _`GitHub pull request documentation`: https://help.github.com/articles/using-pull-requests
.. _`Git merge vs. rebase`: http://mislav.uniqpath.com/2013/02/merge-vs-rebase/
