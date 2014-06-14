Opps Admin Command-line
=======================

*opps-admin.py* is Opps’s command-line utility for administrative tasks.


Usage
-----

*command* should be one of the commands listed in this document. *options*, which is optional, should be zero or more of the options available for the given command.

    opps-admin.py <command> [options]


Getting runtime help
====================

Run *opps-admin.py* help to display usage information and a list of the commands provided by each application.


startproject <projectname>
==========================

Creates a Opps project directory structure for the given project name in the current directory or the given destination.
For example:

    opps-admin.py startproject myproject


Opps will also accept URLs (http, https, ftp) to compressed archives with the project template files, downloading and extracting them on the fly.
