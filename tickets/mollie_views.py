import Mollie
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from Mollie import API
from django.views.decorators.csrf import csrf_exempt

from tickets import utils
from tickets.models import Event, Order, Customer, MollieKey


def pay(request, event_id):
    """Initiates IDEAL transaction

    Params for transaction:
        amount,
        bank_id,
        description,
        report_url,
        return_url,
        profile_key=None

    Returns:

    """
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = Event.objects.get(id=1)
    errors = []
    mollie = Mollie.API.Client()
    mollie.setApiKey(MollieKey.objects.get(id=1).key)

    if request.method == "POST":
        data = {'first_name': request.session['first_name'], 'last_name': request.session['last_name'],
                'email': request.session['email'], 'cart': request.session['cart'],
                'total': request.session['total'], 'event': Event.objects.get(id=event_id)}
        order = utils.create_order(data)
        request.session['order'] = order.id
        request.session['event'] = event_id
        bank = request.POST.get('bank')
        report_url = settings.MOLLIE_REPORT_URL % event_id
        payment = mollie.payments.create({
            'amount': request.session['total'],
            'description': 'My first API payment',
            'redirectUrl': report_url,
            'metadata': {
                'order_nr': order.id
            },
            'method': Mollie.API.Object.Method.IDEAL,
            'issuer': bank,  # e.g. 'ideal_INGBNL2A'
        })

        return HttpResponseRedirect(payment.getPaymentUrl())
    else:
        if 'cart' not in request.session:
            return HttpResponseRedirect(reverse('step1', args=event_id))
        banks = mollie.issuers.all()
        return render_to_response(
            'step3.html', {
                'event': event,
                'errors': errors,
                'banks': banks,
            },
            context_instance=RequestContext(request)
        )


@csrf_exempt
def pay_report(request):
    """
        Is called by ideal when payment was successful
    """
    print request.POST
    try:
        mollie = Mollie.API.Client()
        mollie.setApiKey(MollieKey.objects.get(id=1).key)
        transaction_id = request.POST.get('id')
        payment = mollie.payments.get(transaction_id)
        order_nr = payment['metadata']['order_nr']
        print 'try ' + str(order_nr) + 'trans: ' + str(transaction_id)
        print payment.__dict__
        if payment.isPaid():
            print 'paid :O'
            #
            # At this point you'd probably want to start the process of delivering the product to the customer.
            #
            send_mail('Ticket' + Event.objects.get(id=request.session['event']).name, 'In de bijlage van'
                                                                                      'dit bericht zult u uw'
                                                                                      'ticket vinden in pdf '
                                                                                      'formaat, bij enige '
                                                                                      'problemen stuur een '
                                                                                      'mail naar: '
                                                                                      'SUPERNEP@fake.com',
                      'ticketing@in2systems.nl',
                      [request.session['email']], fail_silently=True)
            order = Order.objects.get(id=order_nr)
            order.payment_status = 'PAI'
            order.save()
            Customer.objects.get_or_create(**{
                'first_name': request.session['first_name'],
                'last_name': request.session['last_name'],
                'email': request.session['email']
            })
            return HttpResponse('Paid')
        elif payment.isPending():
            #
            # The payment has started but is not complete yet.
            #
            print 'pend'
            order = Order.objects.get(id=order_nr)
            order.payment_status = 'PEN'
            order.save()
            return HttpResponse('Pending')
        elif payment.isOpen():
            #
            # The payment has not started yet. Wait for it.
            #
            print 'open'
            order = Order.objects.get(id=order_nr)
            order.payment_status = 'OPE'
            order.save()
            return HttpResponse('Open')
        else:
            #
            # The payment isn't paid, pending nor open. We can assume it was aborted.
            #
            print 'canc'
            order = Order.objects.get(id=order_nr)
            order.payment_status = 'CAN'
            order.save()
            return HttpResponse('Cancelled')

    except API.Error as e:
        print e
        return HttpResponse('API call failed: ' + e.message)