Develop
=======

South Migrations
----------------

`Remember this for every South migration created!`

For every migration created, make the following modifications.

```python

    from django.contrib.auth import get_user_model
    User = get_user_model()


    class Migration(SchemaMigration):

        def forwards(self, orm):
            # reapeat the following for every create or alter table using "user" relation
            db.create_table('app.model', (
                ('user', self.gf('django...ForeignKey')(to=orm["%s.%s" % (User._meta.app_label, User._meta.object_name)])

        models = {
            ...
            # this should replace "auth.user or accounts.customuser"
            "%s.%s" % (User._meta.app_label, User._meta.module_name): {
                'Meta': {'object_name': User.__name__},
            }

            # repeat the following for every freezed model
            "app.model": {
                'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s.%s']"% (User._meta.app_label, User._meta.object_name)})
            }
        }
```

Haystack
---------

`This is required in order to use the default Haystack setup`

The default haystack search template is the same you find in haystack home page, the difference in opps 
is that for every indexed Model you should implement some fields, properties or methods.

**Required for search**

* title (The title used on search result)
* search_category (It can be used to group things on tabs or just to show the category)
* get_absolute_url (The url for search result)
* get_thumb (optional image path for search result)


**Example**

```python

    class MyModel(models.Model):
        title = models.CharField(max_length=255) # implemented as field
        slug = models.SlugField()
        image = models.FileField()

        # implemented as method
        def get_absolute_url(self):
            return "posts/{0}".format(self.slug)

        # implemented as method
        def get_thumb(self):
            return get_thumb_url_or_something(self.image)

        # implemented as property
        @property
        def search_category(self):
            return _(' Blog post')
```

With the above in your model, you can now create your search_indexes and template and choose to index those 
fields/properties/methods or just access directly on template. (see haystack docs)


**Example of search template**


```html

    {% load images_tags %}


    <h2>Search</h2>

    <form method="get" action=".">
        <table>
            <input type="search" id="q" name="q" placeholder="Search" value="{{ request.GET.q}}" required>
            <tr>
                <td>&nbsp;</td>
                <td>
                    <input type="submit" value="Search">
                </td>
            </tr>
        </table>

        {% if query %}
            <h3>Results</h3>

            {% for result in page.object_list %}
                <p>
                  <small>{{ result.object.search_category }}</small><br>
                  {% if result.object.get_thumb %}
                  <a href="{{ result.object.get_absolute_url }}">
                      <img src="{% image_url result.object.get_thumb.archive.url width=100 height=100 %}" alt="{{ result.object.title}}" class="span2" />
                  </a>
                  {% endif %}

                    <a href="{{ result.object.get_absolute_url }}">{{ result.object.title }}</a>
                </p>
            {% empty %}
                <p>No results found.</p>
            {% endfor %}

            {% if page.has_previous or page.has_next %}
                <div>
                    {% if page.has_previous %}<a href="?q={{ query }}&amp;page={{ page.previous_page_number }}">{% endif %}&laquo; Previous{% if page.has_previous %}</a>{% endif %}
                    |
                    {% if page.has_next %}<a href="?q={{ query }}&amp;page={{ page.next_page_number }}">{% endif %}Next &raquo;{% if page.has_next %}</a>{% endif %}
                </div>
            {% endif %}
        {% else %}
            {# Show some example queries to run, maybe query syntax, something else? #}
        {% endif %}
    </form>
```

