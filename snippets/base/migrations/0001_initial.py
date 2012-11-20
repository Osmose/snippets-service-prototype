# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SnippetTemplate'
        db.create_table('base_snippettemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('base', ['SnippetTemplate'])

        # Adding model 'Snippet'
        db.create_table('base_snippet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.SnippetTemplate'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('base', ['Snippet'])

        # Adding model 'SnippetTemplateValue'
        db.create_table('base_snippettemplatevalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('snippet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Snippet'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('base', ['SnippetTemplateValue'])

        # Adding model 'ClientMatchRule'
        db.create_table('base_clientmatchrule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('startpage_version', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('appbuildid', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('build_target', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('locale', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('channel', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('os_version', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('distribution', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('distribution_version', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('base', ['ClientMatchRule'])


    def backwards(self, orm):
        # Deleting model 'SnippetTemplate'
        db.delete_table('base_snippettemplate')

        # Deleting model 'Snippet'
        db.delete_table('base_snippet')

        # Deleting model 'SnippetTemplateValue'
        db.delete_table('base_snippettemplatevalue')

        # Deleting model 'ClientMatchRule'
        db.delete_table('base_clientmatchrule')


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
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.SnippetTemplate']"})
        },
        'base.snippettemplate': {
            'Meta': {'object_name': 'SnippetTemplate'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'base.snippettemplatevalue': {
            'Meta': {'object_name': 'SnippetTemplateValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Snippet']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['base']