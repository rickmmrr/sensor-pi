
import RPi.GPIO as GPIO
import time

relay_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

while True:
    GPIO.output(relay_pin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(relay_pin, GPIO.LOW)
    time.sleep(2)

