from PyPDF2 import PdfFileReader, PdfFileWriter

__author__ = 'Aaron'

import uuid
import StringIO
from qrcode import QRCode, ERROR_CORRECT_L
from reportlab.pdfgen import canvas
from datetime import datetime
from tickets.models import Order, Ticket


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
    create_tickets(data['cart'], order, data['first_name'] + data['last_name'])
    return order


def create_tickets(cart, order, name):
    packet = StringIO.StringIO()
    qr = QRCode(version=1, error_correction=ERROR_CORRECT_L, box_size=50,
    border=4,)

    existing_pdf = PdfFileReader(file("C:\Users\Aaron\Desktop\motopiapdf.pdf", "rb"))
    output = PdfFileWriter()
    output_stream = file(r"C:\Users\Aaron\Desktop\tickets\Order" + str(order.id) + ".pdf", "wb")
    for ticket_type, number in cart.iteritems():
                for index in range(0, int(number)):
                    ticket = Ticket.objects.create(**{
                        'ticket_type_id': ticket_type,
                        'order_id': order.id,
                    })
                    # create a new PDF with Reportlab
                    qr.add_data(uuid.uuid4())
                    qr.make(fit=True)
                    img = qr.make_image()
                    img.save("C:\Users\Aaron\Desktop\tickets\QR\qr.jpg", 'JPEG')
                    can = canvas.Canvas(packet)
                    can.drawImage("C:\Users\Aaron\Desktop\tickets\QR\qr.jpg", 10, 10, 100, 100)
                    can.drawString(40, 150, "Terms :P" + str(name) + "ORDER:" + str(order.id) + "TICKET:" +
                                            str(ticket.id))
                    can.save()
                    # read your existing PDF
                    page = existing_pdf.getPage(0)
                    packet.seek(0)
                    new_pdf = PdfFileReader(packet)
                    page.mergePage(new_pdf.getPage(0))
                    output.addPage(page)
    output.write(output_stream)
    output_stream.close()