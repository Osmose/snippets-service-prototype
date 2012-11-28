# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SnippetLocale'
        db.create_table('base_snippetlocale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='locale_set', to=orm['base.Snippet'])),
            ('locale', self.gf('snippets.base.models.LocaleField')(default='en-US', max_length=32)),
        ))
        db.send_create_signal('base', ['SnippetLocale'])

        # Adding model 'SnippetTemplateLocale'
        db.create_table('base_snippettemplatelocale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='locale_set', to=orm['base.SnippetTemplate'])),
            ('locale', self.gf('snippets.base.models.LocaleField')(default='en-US', max_length=32)),
        ))
        db.send_create_signal('base', ['SnippetTemplateLocale'])


    def backwards(self, orm):
        # Deleting model 'SnippetLocale'
        db.delete_table('base_snippetlocale')

        # Deleting model 'SnippetTemplateLocale'
        db.delete_table('base_snippettemplatelocale')


    models = {
        'base.clientmatchrule': {
            'Meta': {'object_name': 'ClientMatchRule'},
            'appbuildid': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'build_target': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'distribution': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'distribution_version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'exclusion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'startpage_version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        'base.snippet': {
            'Meta': {'object_name': 'Snippet'},
            'client_match_rules': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.ClientMatchRule']", 'symmetrical': 'False', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'on_aurora': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_beta': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_nightly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_release': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_startpage_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_startpage_2': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_startpage_3': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product_name': ('django.db.models.fields.CharField', [], {'default': "'Firefox'", 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'null': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.SnippetTemplate']"})
        },
        'base.snippetlocale': {
            'Meta': {'object_name': 'SnippetLocale'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locale': ('snippets.base.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locale_set'", 'to': "orm['base.Snippet']"})
        },
        'base.snippetsettings': {
            'Meta': {'object_name': 'SnippetSettings'},
            'global_css': ('django.db.models.fields.TextField', [], {}),
            'global_js': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.snippettemplate': {
            'Meta': {'object_name': 'SnippetTemplate'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'null': 'True'})
        },
        'base.snippettemplatelocale': {
            'Meta': {'object_name': 'SnippetTemplateLocale'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locale': ('snippets.base.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locale_set'", 'to': "orm['base.SnippetTemplate']"})
        },
        'base.snippettemplatevariable': {
            'Meta': {'object_name': 'SnippetTemplateVariable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.SnippetTemplate']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['base']