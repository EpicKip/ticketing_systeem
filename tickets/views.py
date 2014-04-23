from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.template import RequestContext
from django.template.response import TemplateResponse
from tickets.models import Event


def index(request):
    events = Event.objects.all()
    return render_to_response('base.html', {'events': events}, context_instance=RequestContext(request))


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            pass
    else:
        # Return an 'invalid login' error message.
        pass


def logout_view(request):
    logout(request)
    request.session.flush()
    request.user = AnonymousUser


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