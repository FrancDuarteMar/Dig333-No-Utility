from escpos.printer import Serial

p = Serial(devfile = "/dev/serial0", baudrate = 19200, bytesize = 8, parity = "N", stopbits = 1, timeout = 1.00, dsrdtr = True)
#p.text("Hello World\n")

# p.set(align = "center",
#      width = 8,
#      height = 8,
#      density = 2)
# p.qr("https://imgur.com/a/MpRMWQ6", native = False, size = 8)

p.image("/home/pi/Desktop/Stable.png")