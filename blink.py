import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
ACTIVE = True
sleepTime = 0.5
try:
    while ACTIVE:
        GPIO.output(23,GPIO.HIGH)
        time.sleep(sleepTime)
        GPIO.output(23,GPIO.LOW)
        time.sleep(sleepTime)

except KeyboardInterrupt:
    GPIO.cleanup()
    quit()
