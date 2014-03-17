# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'pacient'
        db.create_table(u'obpacient_pacient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('p_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('p_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('p_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('p_LMP', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('p_EDC', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('p_diseaseHis', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('p_phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('p_Econtact', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('p_email', self.gf('django.db.models.fields.EmailField')(max_length=1000, blank=True)),
            ('p_state', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('p_conception', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'obpacient', ['pacient'])


    def backwards(self, orm):
        # Deleting model 'pacient'
        db.delete_table(u'obpacient_pacient')


    models = {
        u'obpacient.pacient': {
            'Meta': {'object_name': 'pacient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'p_EDC': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'p_Econtact': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'p_LMP': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'p_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'p_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'p_conception': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'p_diseaseHis': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'p_email': ('django.db.models.fields.EmailField', [], {'max_length': '1000', 'blank': 'True'}),
            'p_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'p_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'p_state': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['obpacient']