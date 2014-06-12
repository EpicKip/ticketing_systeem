import email
from django.core.mail import send_mail

__author__ = 'Aaron'
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response
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
    if 'error1' in request.session or 'error2' in request.session:
        return render(request, 'step1.html', {'event': event, 'eventtickets': eventtickets,
                                              'error1': request.session['error1'], 'error2': request.session['error2']})
    else:
        return render(request, 'step1.html', {'event': event, 'eventtickets': eventtickets})


@event_active()
def step2(request, event_id):
    if 'error1' in request.session:
        del request.session['error1']
    if 'error2' in request.session:
        del request.session['error2']
    try:
        event = Event.objects.get(id=event_id)
        eventtickets = EventTicket.objects.filter(event_id=event_id)
    except Event.DoesNotExist:
        return render(request, "inactive.html")
    if 'csrfmiddlewaretoken' in request.session['cart']:
        del request.session['cart']['csrfmiddlewaretoken']
    subtotal = {}
    total = 0
    error1, error2 = "", ""
    for eventticket in eventtickets:
        cart = request.session['cart']
	number1 = request.session['cart'][str(eventticket.id)][0]
        number2 = EventTicket.objects.get(id=eventticket.id).price
        if "-" in str(number1):
            error1 = "U kunt geen negatief aantal tickets bestellen."
        if float(number1.replace(',', '.')).is_integer() is False:
            error2 = "U kunt alleen een geheel getal aan tickets bestellen."
        else:
            total += int(number1) * int(number2)
            subtotal[str(eventticket.id)] = (float(number1) * float(number2))
    if error1 == "" and error2 == "":
        request.session['total'] = total
        if 'mail_error' in request.session or 'check_error' in request.session:
            return render(request, 'step2.html', {'event': event, 'eventtickets': eventtickets,
                                            'cart': request.session.get('cart'), 'subtotal': subtotal, 'total': total,
                                            'error1': request.session['mail_error'],
                                            'error2': request.session['check_error']})
        else:
            return render(request, 'step2.html', {'event': event, 'eventtickets': eventtickets,
                                            'cart': request.session.get('cart'), 'subtotal': subtotal, 'total': total})
    else:
        request.session['error1'] = error1
        request.session['error2'] = error2
        return HttpResponseRedirect(reverse('step1', args=(event_id,)))


@event_active()
def step4(request, event_id):
    if 1 == 1:
        # msg = email.mime.Multipart.MIMEMultipart()
        # body = email.mime.Text.MIMEText("""In de bijlage vind u een ticket die u uit kunt printen.""")
        # msg.attach(body)
        # filename = Order.objects.get(id=request.session['order']).pdf.path
        # fp = open(filename, 'rb')
        # att = email.mime.application.MIMEApplication(fp.read(), _subtype="pdf")
        # fp.close()
        # att.add_header('Content-Disposition', 'attachment', filename=filename)
        # msg.attach(att)
        send_mail('Ticket' + Event.objects.get(id=event_id).name, 'ticketing@nationevents.nl', 'In de bijlage van'
                                                                                               'dit bericht zult u uw'
                                                                                               'ticket vinden in pdf '
                                                                                               'formaat, bij enige '
                                                                                               'problemen stuur een '
                                                                                               'mail naar: '
                                                                                               'SUPERNEP@fake.com',
        [request.session['email']], fail_silently=True)
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return render(request, "inactive.html")
        if 'email' not in request.session:
            request.session['email'] = ''
        status = ""
        return render(request, 'step4.html', {'event': event, 'email': request.session['email'],
                                              'status': status})


def register(request):
    if request.user.is_authenticated():
        return render_to_response('profile.html', context_instance=RequestContext(request))
    else:
        return render(request, 'register.html')


def set_items(request, event_id):
    cart = request.POST
    new_cart = dict()
    for key, value in cart.iteritems():
	if type(value)==type(list()):
            value = value[0]
        new_cart[key] = value
    request.session['cart'] = new_cart
    return HttpResponseRedirect(reverse('tickets.views.step2', args=(event_id,)))


def mail(request, event_id):
    if 'mail_error' in request.session:
        del request.session['mail_error']
    if 'check_error' in request.session:
        del request.session['check_error']
    mail_error = ""
    check_error = ""
    if request.POST.get('email') is u'':
        mail_error = "You have to enter your email."
    request.session['email'] = request.POST.get('email')
    request.session['first_name'] = request.POST.get('first_name')
    request.session['last_name'] = request.POST.get('last_name')
    if request.POST.get('terms') is None:
        checkbox = 'off'
    else:
        checkbox = request.POST['terms']
    if checkbox == 'on' and request.POST.get('email') is not u'':
        return HttpResponseRedirect(reverse('step3', args=(event_id,)))
    else:
        check_error = "The checkbox has to be checked"
        request.session['mail_error'] = mail_error
        request.session['check_error'] = check_error
        return HttpResponseRedirect(reverse('step2', args=(event_id,)))


def terms(request):
    return render_to_response('terms.html', context_instance=RequestContext(request))


def download(request):
    pdf = Order.objects.get(id=request.session['order'])
    return serve_file(request, pdf.pdf)
