from django.core.exceptions import ValidationError
from django.forms import forms

__author__ = 'aaron'

from django.contrib import admin
from tickets.models import *
from django.contrib.auth import models
from forms import *

class CustomerAdmin(admin.ModelAdmin):
    def name(self, obj):
        return '<a href="%s"> %s </a>' % (obj.user.id, obj.full_name())
    name.allow_tags = True
    list_display = ('id', 'name')
    search_fields = ['id', 'user__first_name', 'user__last_name']

class EventAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'start_time')
    search_fields = ['id', 'name']

class TicketAdmin(admin.ModelAdmin):
    def name(self, obj):
        return '<a href="%s"> %s </a>' % (obj.customer.user.id, obj.full_name())
    name.allow_tags = True
    list_display = ('id', 'event', 'name')
    search_fields = ['id', 'event__name', 'full_name'
    ]


class StaffMemberAdmin(admin.ModelAdmin):
    def name(self, obj):
        return '<a href="%s"> %s </a>' % (obj.user.id, obj.full_name)
    name.allow_tags = True
    list_display = ('name','staff_type',)
    search_fields = ['id', 'staff_type'#, 'name'
    ]
    form = StaffMemberForm

class TicketTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['id', 'name']

    class Media:
        js = [
        'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        'grappelli/tinymce_setup/tinymce_setup.js',
        ]



class EventTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ['id', 'name']

    class Media:
        js = [
        'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        'grappelli/tinymce_setup/tinymce_setup.js',
        ]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(StaffMember, StaffMemberAdmin)
admin.site.register(TicketTemplate, TicketTemplateAdmin)
admin.site.register(EventTemplate, EventTemplateAdmin)
