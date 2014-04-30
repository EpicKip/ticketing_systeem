__author__ = 'aaron'

from django.contrib import admin
from tickets.models import *
from forms import *
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name')
    search_fields = ['id', 'user__first_name', 'user__last_name', 'user__username']

    @staticmethod
    def full_name(instance):
        return instance.user.first_name + " " + instance.user.last_name


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_time')
    search_fields = ['id', 'name']


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'event_name')
    search_fields = ['id', 'event_name', 'full_name']

    @staticmethod
    def event_name(instance):
        return instance.event.name


class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'staff_type', 'event',)
    search_fields = ['id', 'staff_type', 'user__first_name', 'user__last_name', 'user__username']
    list_filter = ['staff_type']
    form = StaffMemberForm

    def save_model(self, request, obj, form, change):
        super(StaffMemberAdmin, self).save_model(request, obj, form, change)
        if obj.the_password:
            messages.add_message(request, messages.INFO, _('The generated password is: %s') % obj.the_password)


class EventTicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'event')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(StaffMember, StaffMemberAdmin)
admin.site.register(EventTicket, EventTicketAdmin)
