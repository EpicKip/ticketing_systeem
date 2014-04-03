__author__ = 'aaron'

from django.contrib import admin
from tickets.models import *
from django.contrib.auth import models

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name')


class EventAdmin(admin.ModelAdmin):
    pass


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name')


class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name','staff_type',)


class TicketTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

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
