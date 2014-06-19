__author__ = 'Aaron'

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from filetransfers.api import serve_file
from tickets.models import EventTicket, Order
from decorators import *


def index(request):
    events = Event.objects.all()
    return render_to_response('base.html', {'events': events}, context_instance=RequestContext(request))


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']
        # Attempt to see if the username/password
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
            return HttpResponseRedirect(request.GET['next'])
        else:
            return render_to_response('login.html', context_instance=RequestContext(request))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@event_active()
def show_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
    return render(request, 'index.html', {'event': event, 'eventticket': EventTicket})


@event_active()
def step1(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        eventtickets = EventTicket.objects.filter(event_id=event_id)
    except Event.DoesNotExist:
        return render(request, "inactive.html")
    #Checking if user is GETting or POSTing
    if request.method == 'GET':
        return render(request, 'step1.html', {'event': event, 'eventtickets': eventtickets})
    elif request.method == 'POST':
        request.session['cart'] = request.POST.copy()
        if 'csrfmiddlewaretoken' in request.session['cart']:
            del request.session['cart']['csrfmiddlewaretoken']
        negative_error, decimal_error = '', ''
        for eventticket in eventtickets:
            number1 = request.session['cart'][str(eventticket.id)]
            if "-" in str(number1):
                negative_error = "U kunt geen negatief aantal tickets bestellen."
            if float(number1.replace(',', '.')).is_integer() is False:
                decimal_error = "U kunt alleen een geheel getal aan tickets bestellen."
        if negative_error == '' and decimal_error == '':
            if all(val[0] == u'0' for val in request.session['cart'].values()):
                no_ticket_error = 'U moet minimaal 1 ticket bestellen'
                return render(request, 'step1.html', {'event': event, 'eventtickets': eventtickets,
                                                      'error1': no_ticket_error})
            else:
                return HttpResponseRedirect(reverse('step2', args=event_id))
        else:
            return render(request, 'step1.html', {'event': event, 'eventtickets': eventtickets, 'error1': decimal_error,
                                                  'error2': negative_error})


@event_active()
def step2(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        eventtickets = EventTicket.objects.filter(event_id=event_id)
    except Event.DoesNotExist:
        return render(request, "inactive.html")
    #Checking if user is GETting or POSTing
    if request.method == 'GET':
        if 'cart' not in request.session:
            return HttpResponseRedirect(reverse('step1', args=event_id))
        else:
            total = 0
            subtotal = {}
            for eventticket in eventtickets:
                number1 = request.session['cart'][str(eventticket.id)]
                number2 = EventTicket.objects.get(id=eventticket.id).price
                total += float(number1) * float(number2)
                subtotal[str(eventticket.id)] = (float(number1) * float(number2))
            request.session['total'] = total
            request.session['subtotal'] = subtotal
            return render(request, 'step2.html', {'event': event, 'eventtickets': eventtickets,
                                                'cart': request.session.get('cart'),
                                                'subtotal': subtotal,
                                                'total': total})
    elif request.method == 'POST':
        mail_error = ""
        check_error = ""
        if request.POST.get('email') is u'':
            mail_error = "U moet uw email invullen"
            request.session['error1'] = mail_error
        request.session['email'] = request.POST.get('email')
        request.session['first_name'] = request.POST.get('first_name')
        request.session['last_name'] = request.POST.get('last_name')
        if request.POST.get('terms') is None:
            check_error = "U moet akkoord gaan met de terms en conditions"
            request.session['error2'] = check_error
        if 'error1' in request.session or 'error2' in request.session:
            return render(request, 'step2.html', {'event': event, 'eventtickets': eventtickets,
                                                'cart': request.session.get('cart'),
                                                'subtotal': request.session['subtotal'],
                                                'total': request.session['total'],
                                                'error1': request.session['error1'],
                                                'error2': request.session['error2']})
        else:
            return HttpResponseRedirect(reverse('step3', args=event_id))


@event_active()
def step4(request, event_id):
    if 1 == 1:
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return render(request, "inactive.html")
        if request.method == 'GET':
            return render(request, 'step4.html', {'event': event, 'email': request.session['email']})
        if request.method == 'POST':
            mail_error = ''
            if request.POST.get('mail') == '':
                mail_error = 'U moet uw email invullen'
            if 'mail_error' is '':
                return render(request, 'step4.html', {'event': event,
                                                'cart': request.session.get('cart'),
                                                'email': request.session['email']})
            else:
                return render(request, 'step4.html', {'event': event, 'error1': mail_error})


def register(request):
    if request.user.is_authenticated():
        return render_to_response('profile.html', context_instance=RequestContext(request))
    else:
        return render(request, 'register.html')


def terms(request):
    return render_to_response('terms.html', context_instance=RequestContext(request))


def download(request):
    pdf = Order.objects.get(id=request.session['order'])
    return serve_file(request, pdf.pdf)