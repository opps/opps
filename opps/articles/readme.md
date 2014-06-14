
Post
====

Not only a simple Post but you can bind separately:

 - Album
 - Container

When rendering Album inside a Post there is a simple rule for the image order:

  1. Post main image
  2. Album main image
  3. Album binded images

Album
=====

Group of Image objects can be binded on other Containers or rendered by itself.

Link
====

Representation of external links(normally) but can point to internal objects(Container).
This behavior is controlled by the flag **is_local**.