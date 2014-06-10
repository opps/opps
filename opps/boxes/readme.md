
QuerySet
========

Queryset is used to gatter automatic data.
It is used together(but not uniquely) with [Containerbox](https://github.com/opps/opps/tree/master/opps/containers) this way we can make the box update by itself based on some params:

 - Model (Which model to get, for example Container/Container or Article/Post)
 - Channel (Specific channel to grab data from)
 - Recursive (Look into this channels childs(subchannels) recursivelly)
 - Filters (Json filters based on [django query language](https://docs.djangoproject.com/en/dev/topics/db/queries/#retrieving-specific-objects-with-filters) will be passed to .filters(**kwargs))
 - Excludes (same as filters but will be passed to .excludes(**kwargs) check the [docs](https://docs.djangoproject.com/en/dev/topics/db/queries/#retrieving-specific-objects-with-filters))
 - Order (Passed to order_by as DESC(-) and ASC(+) if no order_field is passed, it will order by ID)
 - Limit and Offset (Use like you would use python slice [offset:limit])

 More about using it on [Containerbox](https://github.com/opps/opps/tree/master/opps/containers)
