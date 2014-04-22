__author__ = 'Aaron'

from qrcode import *

qr = QRCode(version=20, error_correction=ERROR_CORRECT_L)
qr.add_data("")
qr.make()  # Generate the QRCode itself

# im contains a PIL.Image.Image object
im = qr.make_image()

# To save it
im.save("filename.png")
