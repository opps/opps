from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    complete_apps = ['channels']

    def forwards(self, orm):
        field = self.gf('django.db.models.fields.TextField')
        db.alter_column('channels_channel', 'description', field(null=True))

    def backwards(self, orm):
        field = self.gf('django.db.models.fields.CharField')
        db.alter_column(
            'channels_channel', 'description',
            field(max_length=255, null=True))
