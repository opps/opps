OPPS_FEED_FILTER_DEFAULT
-----------

**Default:** `{}` (empty dict)

Default queryset to "filter" on feed.

**Example:**
```python
OPPS_FEED_FILTER_DEFAULT = {"child_class__in": ["Post", "Mirror"]}
```



OPPS_FEED_EXCLUDE_DEFAULT
-----------

**Default:** `{}` (empty dict)

Default queryset to "exclude" on feed.

**Example:**
```python
OPPS_FEED_EXCLUDE_DEFAULT = {"child_class__in": ["Post", "Mirror"]}
```
