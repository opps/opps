
Cache
=====

Cache in Opps is very simple.
It uses *django.core.cache* and the current pattern to use it is to define a unique **cachekey** based on context and store objects or rendered response in it.

Caching on Templatetags
-----------------------

Example of storing:

    from django.core.cache import cache
    cachekey = "ContainerBox-{}-{}-{}-{}".format(
    	slug,
    	template_name,
    	is_mobile,
    	current_site.id)

    # now we can test if there is something here to render:

    render = cache.get(cachekey)
    if render:
    	return render

    # else we do our business and save in this cachekey

    ...

	render = our_rendered_content
    cache.set(cachekey, render, settings.OPPS_CACHE_EXPIRE)
    return render

To store objects is the same proccess instead of html, you can pass the object list to cache.set and it will work fine.
This method could be used on views too.

Caching Routes
--------------

Caching entire routes is very simple there is a method for that:

    from opps.core.cache import cache_page
    
    (r'^route_pattern$', cache_page(<seconds>)(<page_content>)),

	# real example

	url(r'^(rss|feed)$', cache_page(settings.OPPS_CACHE_EXPIRE)(
        ContainerFeed()), name='feed')

Caching Views
-------------

Caching views are as simples as adding the following decorator above your view function:

	from opps.core.cache import cache_page

    @cache_page(<seconds>)
    def my_view_function():
    	...

Caching inside templates
------------------------

On front you can use cache methods to cache a single fragment of the page like a menu, list or anything that might break your application.

	{% load cache %}
    {% cache <seconds> <cache_identifier> <params> %}
    	...<your content>...
    {% endcache %}

    # real example
	{% cache 3600 menu %}
		...menu here...
	{% endcache %}

You can find much more information about caching on [django docs here](https://docs.djangoproject.com/en/dev/topics/cache/)
    

