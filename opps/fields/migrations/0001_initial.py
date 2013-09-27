# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Field'
        db.create_table(u'fields_field', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('application', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
        ))
        db.send_create_signal(u'fields', ['Field'])

        # Adding model 'Option'
        db.create_table(u'fields_option', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fields.Field'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=140)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'fields', ['Option'])

        # Adding model 'FieldOption'
        db.create_table(u'fields_fieldoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fields.Field'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fields.Option'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'fields', ['FieldOption'])


    def backwards(self, orm):
        # Deleting model 'Field'
        db.delete_table(u'fields_field')

        # Deleting model 'Option'
        db.delete_table(u'fields_option')

        # Deleting model 'FieldOption'
        db.delete_table(u'fields_fieldoption')


    models = {
        u'fields.field': {
            'Meta': {'object_name': 'Field'},
            'application': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'})
        },
        u'fields.fieldoption': {
            'Meta': {'ordering': "['-order']", 'object_name': 'FieldOption'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fields.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fields.Option']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'fields.option': {
            'Meta': {'object_name': 'Option'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fields.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '140'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['fields']