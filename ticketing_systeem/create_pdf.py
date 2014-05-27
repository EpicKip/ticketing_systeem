__author__ = 'Aaron'
import StringIO
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from qrcode import *
from reportlab.pdfgen import canvas


def create_ticket(name, orderid, ticketid):
    packet = StringIO.StringIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet)
    qr = QRCode(version=1, error_correction=ERROR_CORRECT_L, box_size=50,
    border=4,)
    qr.add_data('google.com/funnyfish')
    qr.make(fit=True)  # Generate the QRCode itself
    # im contains a PIL.Image.Image object
    im = qr.make_image()
    im.save("C:\Users\Aaron\Desktop\motopiap.jpg", 'JPEG')
    can.drawImage("C:\Users\Aaron\Desktop\motopiap.jpg", 10, 10, 100, 100)
    can.drawString(40, 150, "Terms :P" + str(name) + "ORDER:" + str(orderid) + "TICKET:" + str(ticketid))
    can.save()
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(file("C:\Users\Aaron\Desktop\motopiapdf.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    return output


        # final = PdfFileWriter()
# output = create_pdf_test.derp(request.session['first_name'] + request.session['last_name'],
#                                               order.id, ticket.id)

                # finally, write "output" to a real file
                # page = output.getPage(0)
                # final.addPage(page)
        #         outputStream = file(r"C:\Users\Aaron\Desktop\tickets\Order" + str(order.id) + ".pdf", "wb")
        # final.write(outputStream)
        # outputStream.close()