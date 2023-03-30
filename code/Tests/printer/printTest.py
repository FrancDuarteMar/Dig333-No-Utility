import serial
uart = serial.Serial("/dev/serial0",baudrate=19200,timeout=3000)
#uart = serial.Serial("/dev/ttyAMA0", baudrate = 19200, timeout = 1)

import adafruit_thermal_printer
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.19)
#ThermalPrinter = adafruit_thermal_printer.thermal_printer_legacy.get_printer_class(2.19)
printer = ThermalPrinter(uart)
# printer.reset()

printer.warm_up()
print("Warm up done")

printer.test_page()
#print(printer.has_paper())
print("DONE")
