![Opps CMS](https://raw.githubusercontent.com/opps/opps/master/docs/_static/new_logo.png)
# Opps - OPen Publishing System

Opps is a platform or toolkit to build a CMS developed with Django, accompanies many packages that aim to meet the need of major 
content portals. Furthermore the Opps has a flexible structure for creating new apps.


Features
---------

* Written in Django
* Container manager (**container** is content type in *Opps CMS*)
* * Save draft and and preview
* * Dynamic custom field, add field in specific container
* WYSIWYG editors (more than one option)
* Container Box manager (Custom channel home page, add dynamic/fix box)
* Channel organization via tree structure (via mptt, unlimited levels)
* Media file manager, default manager images
* * Multi upload
* User permission in Admin, manager site access on admin
* Configurable dashboard (used grappelli admin theme)
* API for custom container types
* Search engine
* Multi-Site (for real)
* SEO friendly URLs and meta data
* Mobile detect
* JVM compatible (via Jython)
* .NET Framework compatible (via IronPython)
* Opps’s admin (used Django Grappelli) interface works with all modern browsers.

Dependencies
-------------

Opps makes use of as few libraries as possible (apart from a standard Django environment), with the following dependencies

* Python 2.7
* Django >=1.5
* Python Imaging Library - for image resizing
* South - for database migrations
* Django Taggit
* Django Mptt


Release Notes
-------------
###### current stable version: 0.2.5

#### Opps 0.2.6 (develop)
* Django 1.6 compatibility
* Grappelli Admin 2.5.3

#### Opps 0.2.5 (stable)
* Django 1.5
* Grappelli Admin 2.4.10

Check here the full [**CHANGELOG**](https://github.com/opps/opps/blob/master/CHANGELOG.rst).

Sites using
-----------

|  |  |  |
| ------------ | ------------- | ------------ |
| [![Portal Virgula](https://raw.githubusercontent.com/opps/opps/master/docs/_static/thumbs/virgula.png)](http://virgula.uol.com.br) | [![Portal Guiame](https://raw.githubusercontent.com/opps/opps/master/docs/_static/thumbs/guiame.png)](http://guiame.com.br) | [![Grupo Troiano](https://raw.githubusercontent.com/opps/opps/master/docs/_static/thumbs/grupotroiano.png)](http://grupotroiano.com.br) |
| [![Troiano](https://raw.githubusercontent.com/opps/opps/master/docs/_static/thumbs/troiano.png)](http://troiano.com.br) | [![Brands and Values](https://raw.githubusercontent.com/opps/opps/master/docs/_static/thumbs/brandsandvalues.png)](http://brandsandvalues.com.br) | [![Brigh Thouse](https://raw.githubusercontent.com/opps/opps/master/docs/_static/thumbs/bhbr.png)](http://brighthouse.com.br) |
| [![Brand Insights](https://raw.githubusercontent.com/opps/opps/master/docs/_static/thumbs/brandins.png)](http://brandinsights.com.br) | [![Jovem Pan](https://raw.githubusercontent.com/opps/opps/master/docs/_static/thumbs/jpam.png)](http://jovempan.com.br) | [![Jovem Pan FM](https://raw.githubusercontent.com/opps/opps/master/docs/_static/thumbs/jpfm.png)](http://jovempanfm.com.br) |
| [![Rede Vida](https://raw.githubusercontent.com/opps/opps/master/docs/_static/thumbs/redevida.png)](http://redevida.com.br) | | |

Source Code
--------
[https://github.com/opps/opps](https://github.com/opps/opps)

Report a bug
--------

The place to create issues is [opps’s github issues](https://github.com/opps/opps/issues). 
The more information you send about an issue, the greater the chance it will get fixed fast.

Getting help
--------
If you are not sure about something, have a doubt or feedback, or just want to ask for a feature, feel free to join 
[our mailing list](http://groups.google.com/group/opps-developers), or, 
if you’re on FreeNode (IRC), you can join the chat [#opps](http://webchat.freenode.net/?channels=opps).

Sponsors
--------
* [YACOWS](http://www.yacows.com.br)
* [Digital Oceans](http://digitalocean.com/)


License
--------

opps is licensed under the [MIT License](http://opensource.org/licenses/MIT)

Copyright (c) 2013 Opps Project. and other contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
