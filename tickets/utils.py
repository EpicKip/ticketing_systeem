__author__ = 'Aaron'
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from ticketing_systeem.settings import MEDIA_URL
import uuid
import StringIO
from qrcode import QRCode, ERROR_CORRECT_L
from reportlab.pdfgen import canvas
from datetime import datetime
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
        'total': data['total']
    })
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
                    #                         str(ticket.id))
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
                    output = create_pdf(name, order.id, ticket.id, event)
                    page = output.getPage(0)
                    final.addPage(page)
                    output_stream = file(r"http\media\temp\pdf\order" + str(order.id) + ".pdf", "wb")
                    final.write(output_stream)
                    output_stream.close()
    return final


def create_pdf(name, orderid, ticketid, event):
    packet = StringIO.StringIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet)
    qr = QRCode(version=1, error_correction=ERROR_CORRECT_L, box_size=50, border=4,)
    qr.add_data(uuid.uuid4())
    qr.make(fit=True)  # Generate the QRCode itself
    # im contains a PIL.Image.Image object
    im = qr.make_image()
    im.save(r"http\media\temp\qr\qr" + str(ticketid) + ".jpg", 'JPEG')
    can.drawImage("http" + MEDIA_URL + r"temp/qr/qr" + str(ticketid) + ".jpg", 10, 10, 100, 100)
    os.remove(r"http\media\temp\qr\qr" + str(ticketid) + ".jpg")
    can.drawString(250, 110, Terms.objects.get(id=1).terms)
    can.drawString(40, 150, str(name))
    can.drawString(40, 135, "OrderNr: " + str(orderid))
    can.drawString(40, 120, "TicketNr: " + str(ticketid))
    can.save()
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(file("http" + event.template.url, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    return output
