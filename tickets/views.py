from datetime import datetime, date
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from tickets.models import Event


def index(request):
    events = Event.objects.all()
    return render_to_response('base.html', {'events': events}, context_instance=RequestContext(request))


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponse("Logged in! Just press back for the time being.. Im gonna fix it soon")
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your ticketing account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        pass


def user_logout(request):
    logout(request)
    return HttpResponse("Logged out! Just press back for the time being.. Im gonna fix it soon")


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
    return render(request, 'indasddex.html', {'event': event})


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


def view_cart(request):
    cart = request.session.get('cart', {})
    # rest of the view


def add_to_cart(request, item_id, quantity):
    cart = request.session.get('cart', {})
    cart[item_id] = quantity
    request.session['cart'] = cart
    # rest of the view