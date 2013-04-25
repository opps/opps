Develop
=======

South Migrations
----------------

.. note:: Remember this for every South migration created!

For every migration created, make the following modifications.

::

    try:
        from django.contrib.auth import get_user_model
    except ImportError: # django < 1.5
        from django.contrib.auth.models import User
    else:
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
                user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s.%s']"% (User._meta.app_label, User._meta.object_name)})
            }
        }

