from tickets.models import EventTicket

__author__ = 'Aaron'

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def get_ticket_from_session_name(eventticket_id):
    try:
        return EventTicket.objects.get(id=eventticket_id).name
    except EventTicket.DoesNotExist:
        return 'Unknown'


@register.simple_tag
def get_ticket_from_session_price(eventticket_id):
    try:
        return EventTicket.objects.get(id=eventticket_id).price
    except EventTicket.DoesNotExist:
        return 'Unknown'
