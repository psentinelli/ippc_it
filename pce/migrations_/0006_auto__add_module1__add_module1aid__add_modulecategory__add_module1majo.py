# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Module1'
        db.create_table(u'pce_module1', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.PceVersion'])),
            ('modulecategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.ModuleCategory'])),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mod1_country', to=orm['ippc.CountryPage'])),
            ('region', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_5', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_6', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_9', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_10', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_12', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_13', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_14', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_15', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_16', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_17', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_18', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_19', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_22', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_23', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_24', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_25', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module1'])

        # Adding model 'Module1Aid'
        db.create_table(u'pce_module1aid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module1', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module1'])),
            ('donoragency', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('titleprj', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module1Aid'])

        # Adding model 'ModuleCategory'
        db.create_table(u'pce_modulecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=400)),
        ))
        db.send_create_signal(u'pce', ['ModuleCategory'])

        # Adding model 'Module1MajorCrops'
        db.create_table(u'pce_module1majorcrops', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module1', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module1'])),
            ('crops', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('propagation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('germplasm', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('consumption', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wooden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('industrial', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('other', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module1MajorCrops'])


    def backwards(self, orm):
        # Deleting model 'Module1'
        db.delete_table(u'pce_module1')

        # Deleting model 'Module1Aid'
        db.delete_table(u'pce_module1aid')

        # Deleting model 'ModuleCategory'
        db.delete_table(u'pce_modulecategory')

        # Deleting model 'Module1MajorCrops'
        db.delete_table(u'pce_module1majorcrops')


    models = {
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'generic.assignedkeyword': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'AssignedKeyword'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': u"orm['generic.Keyword']"}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {})
        },
        u'generic.keyword': {
            'Meta': {'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.countrypage': {
            'Meta': {'ordering': "['name']", 'object_name': 'CountryPage', '_ormbases': [u'pages.Page']},
            'accepted_epporeport': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'accepted_epporeport_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'cn_flag': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'cn_lat': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'cn_long': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'cn_map': ('django.db.models.fields.CharField', [], {'max_length': '550'}),
            'contact_point': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'country_slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'cp_ncp_t_type': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '3'}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'countryeditors+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'region': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'send_reminder': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'pages.page': {
            'Meta': {'ordering': "('titles',)", 'object_name': 'Page'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_menus': ('mezzanine.pages.fields.MenusField', [], {'default': '(2,)', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['pages.Page']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'})
        },
        u'pce.answerbase': {
            'Meta': {'object_name': 'AnswerBase'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Question']"}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Response']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'pce.answerinteger': {
            'Meta': {'object_name': 'AnswerInteger', '_ormbases': [u'pce.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pce.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.answerradio': {
            'Meta': {'object_name': 'AnswerRadio', '_ormbases': [u'pce.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pce.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.answerselect': {
            'Meta': {'object_name': 'AnswerSelect', '_ormbases': [u'pce.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pce.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.answerselectmultiple': {
            'Meta': {'object_name': 'AnswerSelectMultiple', '_ormbases': [u'pce.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pce.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.answertext': {
            'Meta': {'object_name': 'AnswerText', '_ormbases': [u'pce.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pce.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        u'pce.module': {
            'Meta': {'object_name': 'Module'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        u'pce.module1': {
            'Meta': {'object_name': 'Module1'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mod1_country'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_10': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_12': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_13': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_14': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_15': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_16': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_17': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_18': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_19': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_22': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_23': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_24': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_25': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_6': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_9': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modulecategory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.ModuleCategory']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module1aid': {
            'Meta': {'object_name': 'Module1Aid'},
            'amount': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'donoragency': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module1']"}),
            'titleprj': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.module1majorcrops': {
            'Meta': {'object_name': 'Module1MajorCrops'},
            'consumption': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'crops': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'germplasm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industrial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'module1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module1']"}),
            'other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'propagation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wooden': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'pce.modulecategory': {
            'Meta': {'object_name': 'ModuleCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        u'pce.pceversion': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'PceVersion'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pceversion_author'", 'to': u"orm['auth.User']"}),
            'chosen_modules': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'modules'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['pce.Module']"}),
            'completed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pceversion_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'email_facilitator': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'email_pcemanager': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'file_designation': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            'firstname_facilitator': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_facilitated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lastname_facilitator': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name_authority': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_pcemanager': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'projet_date_completation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title_pcemanager': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'version_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'pce.question': {
            'Meta': {'object_name': 'Question'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Category']", 'null': 'True', 'blank': 'True'}),
            'choices': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module']"}),
            'question_type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '200'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'pce.response': {
            'Meta': {'object_name': 'Response'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.CountryPage']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.TextField', [], {})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['pce']