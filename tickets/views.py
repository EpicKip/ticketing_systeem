from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.redirects.models import Redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from tickets.models import Event, EventTicket
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

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
    del request.session['cart']['csrfmiddlewaretoken']
    subtotal = {}
    total = 0
    for eventticket in eventtickets:
        number1 = request.session['cart'][str(eventticket.id)]
        number2 = EventTicket.objects.get(id=eventticket.id).price
        total += float(number1) * float(number2)
        subtotal[str(eventticket.id)] = (float(number1) * float(number2))
    return render(request, 'step2.html', {'event': event, 'eventtickets': eventtickets, 'cart': request.session.get('cart'), 'subtotal': subtotal, 'total': total})


@login_required
def step3_login(request, event_id):
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


def register(request):
    if request.user.is_authenticated():
        return render_to_response('profile.html', context_instance=RequestContext(request))
    else:
        return render(request, 'register.html')


def set_items(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
    request.session['cart'] = request.POST
    return HttpResponseRedirect(reverse('tickets.views.step2', args=(event_id,)))


def mail(request, event_id):
    # send_mail('Subject here', 'Here is the message.', 'from@example.com',
    # ['to@example.com'], fail_silently=False)
    return HttpResponseRedirect(reverse('tickets.views.step2_3', args=(event_id,)))


def step2_3(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
    request.session['mail'] = False
    request.session['accept'] = request.POST
    print request.session['accept']['terms']
    print request.session['mail']
    try:
        accept = request.session['accept']['terms']
    except ObjectDoesNotExist:
        accept = "No"
    if accept is "Yes":
        return render(request, 'step2_3.html', {'event': event})
    else:
        pass

