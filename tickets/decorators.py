__author__ = 'Aaron'
from django.shortcuts import render
from functools import wraps
from tickets.models import Event


def event_active():
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            event = Event.objects.get(id=kwargs['event_id'])
            if event.event_active is True:
                return func(request, *args, **kwargs)
            else:
                return render(request, "inactive.html")
        return wraps(func)(inner_decorator)
    return decorator
