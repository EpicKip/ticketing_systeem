from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from tickets.models import Event, EventTicket


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
        # If None, no user with matching credentials was found.
        if user is not None:
            # Is the account active?
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the event page.
                login(request, user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                # An inactive account was used - no logging in!
                return render_to_response('login.html', {'errormsg': "Your account has been disabled, contact an admin"
                                                                     "istrator for more info"},
                                          context_instance=RequestContext(request))
        else:
            # Bad login details were provided. So we can't log the user in.
            return render_to_response('login.html', {'errormsg': "Username or password wrong, please try again or"
                                                                 " use the forgot option"},
                                      context_instance=RequestContext(request))

    else:
        # If the user goes to accounts/login show him the login page
        if request.user.is_authenticated():
            return render_to_response('profile.html', context_instance=RequestContext(request))
        else:
            return render_to_response('login.html', context_instance=RequestContext(request))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def show_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
    return render(request, 'index.html', {'event': event, 'eventticket': EventTicket})


def step1(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        eventtickets = EventTicket.objects.filter(event_id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
        eventtickets = EventTicket.objects.filter(event_id=1)
    return render(request, 'step1.html', {'event': event, 'eventtickets': eventtickets})


def step2(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        eventtickets = EventTicket.objects.filter(event_id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
        eventtickets = EventTicket.objects.filter(event_id=1)
    new_dict = {eventtickets.id: request.session.get('cart')[eventtickets.id] for eventtickets in eventtickets}
    return render(request, 'step2.html', {'event': event, 'eventtickets': eventtickets, 'cart': new_dict})


@login_required
def step3(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
    return render(request, 'step3.html', {'event': event})


@login_required
def step4(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
    return render(request, 'step4.html', {'event': event})


def view_cart(request):
    cart = request.session.get('cart', {})


def add_to_cart(request, item_id, quantity):
    cart = request.session.get('cart', {})
    cart[item_id] = quantity
    request.session['cart'] = cart


def register(request):
    if request.user.is_authenticated():
        return render_to_response('profile.html', context_instance=RequestContext(request))
    else:
        return render(request, 'register.html')


def mid_step(request):
    if request.method == 'POST':
        if request.POST['Email'] is '':
            return render_to_response('mid-step.html', context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(request.get_full_path())


def set_itmes(request):
    request.session['cart'] = request.POST
    return render_to_response('step2.html', context_instance=RequestContext(request))


def test(request):
    print(request.session.get('cart'))
    return HttpResponse("derp")