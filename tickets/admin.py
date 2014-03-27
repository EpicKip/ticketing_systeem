__author__ = 'aaron'

from django.contrib import admin
from models import *


class CustomerAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    pass


class TicketAdmin(admin.ModelAdmin):
    pass


class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name','staff_type',)



class TickettemplatetAdmin(admin.ModelAdmin):
    pass

class EventtemplateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(StaffMember, StaffMemberAdmin)
admin.site.register(TicketTemplate, TickettemplatetAdmin)
admin.site.register(EventTemplate, EventtemplateAdmin)
