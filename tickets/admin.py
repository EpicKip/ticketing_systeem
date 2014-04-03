from django.core.exceptions import ValidationError
from django.forms import forms

__author__ = 'aaron'

from django.contrib import admin
from tickets.models import *
from django.contrib.auth import models

class CustomerAdmin(admin.ModelAdmin):
    def name_clickable(self, obj):
        return '<a href="%s"> %s </a>' % (obj.user.id, obj.full_name())
    name_clickable.allow_tags = True
    list_display = ('id', 'name_clickable')


class EventAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'start_time')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'full_name')


class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name','staff_type',)


class TicketTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    class Media:
        js = [
        'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        'grappelli/tinymce_setup/tinymce_setup.js',
        ]



class EventTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

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
