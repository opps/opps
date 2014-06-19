# Opps - OPen Publishing System

Opps is a platform or toolkit to build a CMS developed with Django, accompanies many packages that aim to meet the need of major 
content portals. Furthermore the Opps has a flexible structure for creating new apps.


Features
---------

* Write in Django
* Containar manager (**container** is content type in *Opps CMS*)
* * Save draft and and preview
* * Dynamic custom field, add field in specific container
* WYSIWYG editing (more one option)
* Container Box manager (Custom channel home page, add dynamic/fix box)
* Channel organize via tree (via mptt, not level limit)
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

Dependencies
-------------

Opps makes use of as few libraries as possible (apart from a standard Django environment), with the following dependencies

* Python 2.7
* Django >= 1.5
* Python Imaging Library - for image resizing
* South - for database migrations
* Django Taggit
* Django Mptt


Support
--------

Opps’s admin (used Django Grappelli) interface works with all modern browsers.


Sites using
-----------

* [Portal Virgula](http://virgula.uol.com.br)
* [Portal Guiame](http://guiame.com.br)
* [Grupo Troiano](http://grupotroiano.com.br)
* [Troiano](http://troiano.com.br)
* [Brands and Values](http://brandsandvalues.com.br)
* [Brigh Thouse](http://brighthouse.com.br)
* [Brand Insights](http://brandinsights.com.br)
* [JovemPan AM](http://jovempan.com.br)
* [JovemPan FM](http://jovempanfm.com.br)
* [Rede Vida](http://www.redevida.com.br)


Contact
--------

The place to create issues is [opps’s github issues](https://github.com/opps/opps/issues). 
The more information you send about an issue, the greater the chance it will get fixed fast.

If you are not sure about something, have a doubt or feedback, or just want to ask for a feature, feel free to join 
[our mailing list](http://groups.google.com/group/opps-developers), or, 
if you’re on FreeNode (IRC), you can join the chat [#opps](http://webchat.freenode.net/?channels=opps).

Sponsor
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
