import Mollie
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from ticketing_systeem import settings
from tickets.models import Event, Order, Ticket


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
    mollie.setApiKey('test_Wsultq8WxKJPvWzBhd5ypbyX1606Ux')

    if request.method == "POST":
        #Order maken en session['cart'] naar text veld in order tabel schijven - datum&tijd - Status - Gebruiker info
        order = Order.objects.create(**{
            'first_name': request.session['first_name'],
            'last_name': request.session['last_name'],
            'email': request.session['email'],
            'date_time': datetime.now(),
            'payment_status': 'OPE',
            'raw_order': request.session['cart'],
            'total': request.session['total']
        })
        cart = request.session['cart']
        for ticket_type, number in cart.iteritems():
            for index in range(0, int(number)):
                Ticket.objects.create(**{
                    'ticket_type_id': ticket_type,
                    'order_id': order.id,
                })
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
        # todo: Add transaction number to order
        return HttpResponseRedirect(payment.getPaymentUrl())
    else:
        #ideal = IDeal(partner_id=settings.IDEAL_PARTNER_ID, testmode=settings.MOLLIE_TEST_MODE)
        banks = mollie.issuers.all()

        return render_to_response(
            'step3.html', {
                'event': event,
                'errors': errors,
                'banks': banks,
            },
            context_instance=RequestContext(request)
        )


def pay_report(request):
    """
    Is called by ideal when payment was successful
    """
    if request.method == 'POST':
        mollie = Mollie.API.Client()
        mollie.setApiKey('test_Wsultq8WxKJPvWzBhd5ypbyX1606Ux')
        transaction_id = request.POST.get('id')
        transaction = mollie.payments.get(transaction_id)
        order_nr = transaction['metadata']['order_nr']
        try:
            order = Order.objects.get(transaction_id=transaction_id)
        except Order.DoesNotExist:
            raise Exception(_("There is no order that matches the transaction ID"))

    if data['payed']:
        invoice.status_id = STATUS_PAID
        invoice.save()

    return HttpResponse(json.dumps(data), mimetype="application/json")