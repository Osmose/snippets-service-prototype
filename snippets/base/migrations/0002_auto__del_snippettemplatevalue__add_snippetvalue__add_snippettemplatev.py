# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SnippetTemplateValue'
        db.delete_table('base_snippettemplatevalue')

        # Adding model 'SnippetValue'
        db.create_table('base_snippetvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('snippet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Snippet'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('base', ['SnippetValue'])

        # Adding model 'SnippetTemplateVariable'
        db.create_table('base_snippettemplatevariable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.SnippetTemplate'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('base', ['SnippetTemplateVariable'])


    def backwards(self, orm):
        # Adding model 'SnippetTemplateValue'
        db.create_table('base_snippettemplatevalue', (
            ('snippet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Snippet'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base', ['SnippetTemplateValue'])

        # Deleting model 'SnippetValue'
        db.delete_table('base_snippetvalue')

        # Deleting model 'SnippetTemplateVariable'
        db.delete_table('base_snippettemplatevariable')


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
        'base.snippettemplatevariable': {
            'Meta': {'object_name': 'SnippetTemplateVariable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.SnippetTemplate']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'base.snippetvalue': {
            'Meta': {'object_name': 'SnippetValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Snippet']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['base']