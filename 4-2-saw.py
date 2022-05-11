import RPi.GPIO as GPIO
import time as time

GPIO.setmode(GPIO.BCM)

dac = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

try:
    period = int(input("Enter period: "))
    while True:
        for i in range (256):
            b = decimal2binary(i)
            GPIO.output(dac, b)
            time.sleep(period/(256))
    c=input()
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()