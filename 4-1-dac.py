import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

dac = [26, 19, 13, 6, 5, 11, 9, 10]

for D in dac:
    GPIO.setup(D, GPIO.OUT)

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

try:
    n = int(input("Enter number in range 0 - 255: "))
    if(n<0 or n>255):
        print("Diapason error")
        raise ValueError("Diapason error")
         
    GPIO.output(dac, decimal2binary(n))
    print("Answer: ")
    print(3.3/256*n)
    c=input()
except ValueError():
    print("Diapason error")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()

