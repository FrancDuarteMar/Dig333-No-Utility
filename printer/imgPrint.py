from escpos.printer import Serial
from PIL import Image

p = Serial(devfile='/dev/serial0',
           baudrate=19200,
           bytesize=8,
           parity='N',
           stopbits=1,
           timeout=1.00,
           dsrdtr=True
)
size = 768, 512

with Image.open("picture.png") as img:
    img.thumbnail(size)
    p.image(img)