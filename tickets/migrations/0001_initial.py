# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table(u'tickets_customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'tickets', ['Customer'])

        # Adding model 'Event'
        db.create_table(u'tickets_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('sales_start', self.gf('django.db.models.fields.DateField')()),
            ('sales_end', self.gf('django.db.models.fields.DateField')()),
            ('event_active', self.gf('django.db.models.fields.BooleanField')()),
            ('information', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'tickets', ['Event'])

        # Adding model 'EventTicket'
        db.create_table(u'tickets_eventticket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tickets.Event'])),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('maximum', self.gf('django.db.models.fields.IntegerField')()),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'tickets', ['EventTicket'])

        # Adding model 'Ticket'
        db.create_table(u'tickets_ticket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticket_active', self.gf('django.db.models.fields.BooleanField')()),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tickets.Customer'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tickets.Event'])),
            ('template', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'tickets', ['Ticket'])

        # Adding model 'StaffMember'
        db.create_table(u'tickets_staffmember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tickets.Event'])),
            ('staff_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'tickets', ['StaffMember'])


    def backwards(self, orm):
        # Deleting model 'Customer'
        db.delete_table(u'tickets_customer')

        # Deleting model 'Event'
        db.delete_table(u'tickets_event')

        # Deleting model 'EventTicket'
        db.delete_table(u'tickets_eventticket')

        # Deleting model 'Ticket'
        db.delete_table(u'tickets_ticket')

        # Deleting model 'StaffMember'
        db.delete_table(u'tickets_staffmember')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                            {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",
                     'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': (
                'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True',
                        'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True',
                                  'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tickets.customer': {
            'Meta': {'object_name': 'Customer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'tickets.event': {
            'Meta': {'object_name': 'Event'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'event_active': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sales_end': ('django.db.models.fields.DateField', [], {}),
            'sales_start': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'tickets.eventticket': {
            'Meta': {'object_name': 'EventTicket'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tickets.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'maximum': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.FloatField', [], {})
        },
        u'tickets.staffmember': {
            'Meta': {'object_name': 'StaffMember'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tickets.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staff_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'user': ('django.db.models.fields.related.ForeignKey', [],
                     {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'tickets.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tickets.Customer']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tickets.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'ticket_active': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['tickets']