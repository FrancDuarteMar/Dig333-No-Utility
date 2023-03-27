import RPi.GPIO as GPIO

from time import sleep

BUTTON_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUTTON_PIN,GPIO.IN, pull_up_down=GPIO.PUD_UP)
prev_state = GPIO.input(BUTTON_PIN)

while True:
    sleep(1)
    print(GPIO.input(BUTTON_PIN))