# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ArticleBoxArticles.date_available'
        db.add_column(u'articles_articleboxarticles', 'date_available',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True),
                      keep_default=False)

        # Adding field 'ArticleBoxArticles.date_end'
        db.add_column(u'articles_articleboxarticles', 'date_end',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ArticleBoxArticles.date_available'
        db.delete_column(u'articles_articleboxarticles', 'date_available')

        # Deleting field 'ArticleBoxArticles.date_end'
        db.delete_column(u'articles_articleboxarticles', 'date_end')


    models = {
        "%s.%s" % (User._meta.app_label, User._meta.module_name): {
        'Meta': {'object_name': User.__name__},
        },
        u'articles.album': {
            'Meta': {'ordering': "['-date_available', 'title', 'channel_long_slug']", 'object_name': 'Album', '_ormbases': [u'articles.Article']},
            u'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['articles.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'articles.article': {
            'Meta': {'ordering': "['-date_available', 'title', 'channel_long_slug']", 'unique_together': "(['site', 'child_class', 'channel_long_slug', 'slug'],)", 'object_name': 'Article'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['channels.Channel']"}),
            'channel_long_slug': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'channel_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'child_app_label': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'child_class': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'hat': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'article_images'", 'to': u"orm['images.Image']", 'through': u"orm['articles.ArticleImage']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['images.Image']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['sources.Source']", 'null': 'True', 'through': u"orm['articles.ArticleSource']", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)})
        },
        u'articles.articlebox': {
            'Meta': {'object_name': 'ArticleBox'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['articles.Article']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'articlebox_articles'", 'to': u"orm['articles.Article']", 'through': u"orm['articles.ArticleBoxArticles']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['channels.Channel']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'channel_long_slug': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'db_index': 'True'}),
            'channel_name': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'db_index': 'True'}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'queryset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boxes.QuerySet']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)})
        },
        u'articles.articleboxarticles': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ArticleBoxArticles'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'articleboxarticles_articles'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['articles.Article']"}),
            'articlebox': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'articleboxarticles_articleboxes'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['articles.ArticleBox']"}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'articles.articleconfig': {
            'Meta': {'unique_together': "(('key_group', 'key', 'site', 'channel', 'article'),)", 'object_name': 'ArticleConfig'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['articles.Article']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['channels.Channel']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'}),
            'key_group': ('django.db.models.fields.SlugField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'articles.articleimage': {
            'Meta': {'object_name': 'ArticleImage'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'articleimage_articles'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['articles.Article']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['images.Image']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'articles.articlesource': {
            'Meta': {'object_name': 'ArticleSource'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'articlesource_articles'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['articles.Article']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'articlesource_sources'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['sources.Source']"})
        },
        u'articles.link': {
            'Meta': {'ordering': "['-date_available', 'title', 'channel_long_slug']", 'object_name': 'Link', '_ormbases': [u'articles.Article']},
            u'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['articles.Article']", 'unique': 'True', 'primary_key': 'True'}),
            'articles': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'link_article'", 'null': 'True', 'to': u"orm['articles.Article']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'articles.post': {
            'Meta': {'ordering': "['-date_available', 'title', 'channel_long_slug']", 'object_name': 'Post', '_ormbases': [u'articles.Article']},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'post_albums'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['articles.Album']"}),
            u'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['articles.Article']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'related_posts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'post_relatedposts'", 'to': u"orm['articles.Post']", 'through': u"orm['articles.PostRelated']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        u'articles.postrelated': {
            'Meta': {'object_name': 'PostRelated'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'postrelated_post'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['articles.Post']"}),
            'related': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'postrelated_related'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['articles.Post']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'boxes.queryset': {
            'Meta': {'object_name': 'QuerySet'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['channels.Channel']"}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '7'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)})
        },
        u'channels.channel': {
            'Meta': {'object_name': 'Channel'},
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'homepage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'long_slug': ('django.db.models.fields.SlugField', [], {'max_length': '250'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'subchannel'", 'null': 'True', 'to': u"orm['channels.Channel']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'show_in_menu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'images.image': {
            'Meta': {'object_name': 'Image'},
            'crop_example': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fit_in': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'flip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'halign': ('django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '6', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'smart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sources.Source']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)}),
            'valign': ('django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '6', 'null': 'True', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'sources.source': {
            'Meta': {'object_name': 'Source'},
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'feed': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['articles']