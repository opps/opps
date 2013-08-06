# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'tags_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_insert', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'tags', ['Tag'])

        # Adding unique constraint on 'Tag', fields ['slug', 'name']
        db.create_unique(u'tags_tag', ['slug', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['slug', 'name']
        db.delete_unique(u'tags_tag', ['slug', 'name'])

        # Deleting model 'Tag'
        db.delete_table(u'tags_tag')


    models = {
        u'tags.tag': {
            'Meta': {'unique_together': "(['slug', 'name'],)", 'object_name': 'Tag'},
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['tags']