__author__ = 'Aaron'
import os
import uuid
import StringIO
from datetime import datetime

from PyPDF2 import PdfFileReader, PdfFileWriter
from qrcode import QRCode, ERROR_CORRECT_L
from reportlab.pdfgen import canvas
from django.conf import settings

from ticketing_systeem.base import MEDIA_URL
from tickets.models import Order, Ticket, Terms


def password_random(string_length):
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-", "")
    return random[0:string_length]


def create_order(data):
    order = Order.objects.create(**{
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email'],
        'date_time': datetime.now(),
        'payment_status': 'OPE',
        'raw_order': data['cart'],
        'total': data['total'],
    })
    order.pdf = os.path.join(settings.PDF_LOCATION, "pdf", "order" + str(order.id) + '.pdf')
    order.save()
    final = PdfFileWriter()
    create_tickets(data['cart'], order, data['first_name'] + data['last_name'], final, data['event'])
    return order


def create_tickets(cart, order, name, final, event):
    for ticket_type, number in cart.iteritems():
        for index in range(0, int(number)):
            ticket = Ticket.objects.create(**{
                'ticket_type_id': ticket_type,
                'order_id': order.id,
            })
            # # create a new PDF with Reportlab
            # output = PdfFileWriter()
            # qr = QRCode(version=1, error_correction=ERROR_CORRECT_L, box_size=50,
            # border=4,)
            # packet = StringIO.StringIO()
            # qr.add_data(uuid.uuid4())
            # qr.make(fit=True)
            # img = qr.make_image()
            # img.save(r"C:\Users\Aaron\Desktop\tickets\QR\qr.jpg", 'JPEG')
            # can = canvas.Canvas(packet)
            # can.drawImage(r"C:\Users\Aaron\Desktop\tickets\QR\qr.jpg", 10, 10, 100, 100)
            # can.drawString(40, 150, "Terms :P" + str(name) + "ORDER:" + str(order.id) + "TICKET:" +
            # str(ticket.id))
            # can.save()
            # # read your existing PDF
            # page = existing_pdf.getPage(0)
            # packet.seek(0)
            # new_pdf = PdfFileReader(packet)
            # page.mergePage(new_pdf.getPage(0))
            # output.addPage(page)
            # page = output.getPage(0)
            # final.addPage(page)
            # final = PdfFileWriter()
            output = create_pdf(name, order.id, ticket.id, event, ticket.ticket_type.name)
            page = output.getPage(0)
            final.addPage(page)
            output_stream = file(os.path.join(settings.PDF_LOCATION, "pdf", "order" + str(order.id) + ".pdf"), "wb")
            final.write(output_stream)
            output_stream.close()
    return final


def create_pdf(name, orderid, ticketid, event, tickettype):
    packet = StringIO.StringIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet)
    qr = QRCode(version=1, error_correction=ERROR_CORRECT_L, box_size=50, border=4, )
    qr.add_data(uuid.uuid4())
    qr.make(fit=True)  # Generate the QRCode itself
    # im contains a PIL.Image.Image object
    im = qr.make_image()
    im.save(r"http\media\temp\qr\qr" + str(ticketid) + ".jpg", 'JPEG')
    can.drawImage("http" + MEDIA_URL + r"temp/qr/qr" + str(ticketid) + ".jpg", 150, 50, 125, 125)
    os.remove(r"http\media\temp\qr\qr" + str(ticketid) + ".jpg")
    terms = Terms.objects.get(id=1).terms
    terms = terms.replace('\r\n', 'SPLIT')
    terms = terms.split("SPLIT")
    x = 150
    for line in terms:
        can.drawString(300, x, line)
        x -= 15
    can.drawString(20, 150, str(name))
    can.drawString(20, 135, "OrderNr: " + str(orderid))
    can.drawString(20, 120, "TicketNr: " + str(ticketid))
    can.drawString(20, 30, "Type: " + str(tickettype))
    can.line(290, 160, 290, 5)
    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(file(event.template.path, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    return output
