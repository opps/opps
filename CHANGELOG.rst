=========
Changelog
=========

0.2.3
=====

* Add custom sitemap view and OPPS_SITEMAP_LANGUAGE and OPPS_SITEMAP_PUBLICATION_NAME params
* Create template tag `exclude_queryset_by` on Containers application
* Create template tag `filter_queryset_by` on Containers application
* Change API Engine restframework to piston
* * Easier to polymorphic work
* * Old api removed
* * Create `opps.api.ApiKeyAuthentication`
* Add Atom feed urls #119
* Fix image_obj template tag when sending Nonetype image
* Create Opps Vagrant box to help other contributors
* Added support to ajax requests with extends_parent variable in template context
* Write logging contrib application #275
* Fixed run tests on celery, because use Calling Tasks
* Update fixture example
* Fix test running on Django 1.5, 1.6 and 1.7 #145
* * Change test folder, opps/<application>/tests to tests/<application>
* * Used nose
* Create `OPPS_CORE_APPS`, recommend used on INSTALLED_APPS
* Get queryset (boxes) on get_containerbox (template tags containers), if exist queryset (on containerbox)
* Change ChannelListFilter. Now every parent channel will have an additional /* value on the lookups values
* Add context `breadcrumb` on get_context_data generic views (base)
* Add try_values and cache_obj template tags
* Change BaseBoxAdmin queryset permissions
* opps.contrib.mobile.middleware do not change ``settings.TEMPLATE_DIRS`` on the fly any more, it now use a thread-local variable
* Fix breadcrumb context variable
* Fix template tag `get_post_content`, change folder name articles to containers (Standard Opps 0.2.x)
* Fix filter_queryset_by and exclude_queryset_by when queryset is sliced
* Added extra_context to get_containerbox template tag
* Fix spaced and empty string tags creation
* Fix embedded album image order on Posts
* Containers in home page have direct url without channel, example: site.com/content_slug.html instead of site.com/home/content_slug.html
* Fix url pattern from flatpages, now accept slugs with dashs
* Add `get_custom_field_value` template tag

0.2.2
=====

* Used argparse on opps-admin.py (bin) #82
* Fix test running on Django >= 1.6 #145
* More one channel per container (multi channel)
* Added raw_id_fields on ConfigAdmin
* fix bug, wrong crop params on image_obj templatetag, added lists of valid values
* Add field `title_url` on class model `ContainerBox`
* fix typo, settings_local.py with the wrong index for the database password 'PASS' is correct and 'PASSWORD'
* fix bug "List index out of range" in template tag get_containerbox_list
* Fix bug, mobile detect not bringing this path (url) #265
* Fix sitemaps and added a sitemaps index view
* Fix migration (auto user), ContainerBoxContainers add field highlight

0.2.1
=====

* Add method ``get_http_absolute_url`` on channel model class
* Fix sitemap
* Remove contrib/db_backend , move to opps/db/backends #240
* Fix migrate run on postgresql - articles
* Add ChannelListFilter on HideContainerAdmin list_filter
* Add lazy translation on child_class list_display on HideContainerAdmin
* Add OPPS_CONTAINERS_BLACKLIST config on HideContainerAdmin
* Fix: image crop example
* Used get_descendants (mptt) on generic base view
* changing datetime.now to timezone.now on search index
* Fix unicode treatment JSONField rendering
* Write test on ``opps.db._redis``
* Set dynamic db int, on db drive
* Fix: get_child recursivelly on template tag ``get_container_by_channel``
* Changelog organize
* Fix docs organize
* Remove Opps theme docs, used default Read the Docs

0.2.0
=====

* Content type (Container)
* Isoled boxes application
* ContainerBox, generic box (concept)
* Used Container in all application
* Archives, file manager
* Images used archives
* Used RST on README, pypi compatibility
* Add contrib pattern (like django)
* Upgrade haystack to 2.0 (stable)
* Opps Generic Views
* New view format, used to URLs pattern
* Add Grappelli dependence of the project
* Create Opps DB (NoSQL Database architecture)
* Add redis support (Opps BD)
* Contrib notification, central message exchange between container
* * websocket support
* * sse support
* * long pulling support
* Add field highlight on ContainerBox option
* Fix bug generic view list, get recursive channel list
* Dynamic fields on container, via JSONField
* * Text
* * Textarea
* * Checkbox
* * Radio
* Fix template tag ``image_obj``
* Add optional container filtering by child_class in ListView
* fix flatpage url
* Adding .html in containers url

0.1.9
=====

0.1.8
=====

* Queryset cache on generic view
* Add image thumb on ArticleBox
* Send current site to template ``{{ SITE }}``
* In /rss feed, filter channels by **published** and **include_in_main_rss**
* RSS Feed now renders in a template
* Flatpage is content type Article
* **Hotfix** fix *memory leak* (articles generic view)
* Chekc OPPS_PAGINATE_NOT_APP app not used PAGINATE_SUFFIX
* Used cache page

0.1.7
=====

0.1.6
=====

0.1.5
=====

0.1.4
=====

0.1.3
=====

0.1.0
=====

* Initial release
