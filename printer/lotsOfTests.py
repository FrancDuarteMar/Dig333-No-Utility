import serial
import adafruit_thermal_printer as atp
from escpos.printer import Serial
p = Serial(devfile='/dev/serial0',
           baudrate=19200,
           bytesize=8,
           parity='N',
           stopbits=1,
           timeout=1.00,
           dsrdtr=True
)
uart = serial.Serial("/dev/serial0",baudrate = 19200, timeout = 3000)
ThermalPrinter = atp.get_printer_class(2.19)

printer = ThermalPrinter(uart)
printer.size = atp.SIZE_LARGE
test = "Hello this is the code that should be written to the page printer beause its what. I lied about being needed cuase i iddin;'t knbw what else to do "


printer.print(test)
printer.feed(4)
printer.justify = atp.JUSTIFY_CENTER
printer.size = atp.SIZE_LARGE
printer.print("hello")
printer.feed(4)
p.set(
        align="center",
        font="a",
        width=2,
        height=2,
        density=2,
        invert=0,
        smooth=False,
        flip=False,  
)
p.qr("Circuit Digest",native=True,size=12)
printer.feed(4)