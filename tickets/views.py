from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.template.response import TemplateResponse
from tickets.models import Event


def index(request):
    events = Event.objects.all()
    return render_to_response('index.html', {'events': events}, context_instance=RequestContext(request))


def show_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
    return render(request, 'index.html', {'event': event})


def step2(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
    return render(request, 'index.html', {'event': event})


def step3(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
    return render(request, 'index.html', {'event': event})


def step4(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
    return render(request, 'index.html', {'event': event})