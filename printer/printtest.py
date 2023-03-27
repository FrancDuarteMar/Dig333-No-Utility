import os
os.system("stty -F /dev/serial0 19200")

os.system("echo 'This is a test.' | lp")
