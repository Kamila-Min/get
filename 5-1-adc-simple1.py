import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
maxvoltage = 3.3
troykaModule = 17
comparator = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(troykaModule, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)

def decimal2binary(decimal):
    return [int(bit) for bit in bin(value)[2:].zfill(bits)]


def num2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac,signal)
    return signal


try:
    
    while True:
        for value in range(256):
            signal = num2dac(value)
            
            time.sleep(0.005)
            comparatorValue = GPIO.input(comparator)
            
            if comparatorValue == 0:
                voltage = value/ levels*maxvoltage
                print("ADC value = {:^} -> {}, input voltage = {:2f}".format(value,signal,voltage))
                break

except KeyboardInterrupt:
    print('\nThe programm was stopped by the keyboard')
else:
    print("No exceptions")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print('GPIO cleanup completed')
  
