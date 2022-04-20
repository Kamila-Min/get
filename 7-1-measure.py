import RPi.GPIO as GPIO
import matplotlib.pyplot as plot
import time

MAXVOLT = 3.3

GPIO.setmode (GPIO.BCM)

dac = [26, 19, 13,  6,  5, 11,  9, 10]
leds = [21, 20, 16, 12,  7,  8, 25, 24]
comp = 4
troyka = 17
# настройка GPIO
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)

GPIO.setup(comp, GPIO.IN)

# перевод десятичного числа в бинарный список
def decimal2binary (value):
    return [int(num) for num in bin(value)[2:].zfill(8)]

# перевод двоичного напряжения в напряжение в вольтах
def voltage (bin):
    value = 0
    for i in range (8):
        value += bin[i] / (2 ** (i + 1))     

    return value * MAXVOLT

# определение напряжения на тройка-модуле в двоичном предсавлении
def adc ():
    vol = [0, 0, 0, 0, 0, 0, 0, 0]
    
    for i in range (8):
        vol[i] = 1
        GPIO.output(dac, vol)
        time.sleep(0.005)
        
        if (GPIO.input(comp) == 0):
           vol[i] = 0

    GPIO.output(leds, vol)
    return vol

#вывод значения напряжения на leds
def outputLeds (bin):
    GPIO.output(leds, bin)

try:
    startTime = time.time ()
    measure = []
    numItem = 0
#зарядка конденсатора
    GPIO.output (troyka, 1)

    voltageTroyka = voltage (adc ())
    while (voltageTroyka < 0.95 * MAXVOLT):
        numItem += 1
        print (voltageTroyka)
        measure.append (voltageTroyka)
        voltageTroyka = voltage (adc ())
#разрядка конденсатора
    GPIO.output (troyka, 0)

    while (voltageTroyka > 0.02 * MAXVOLT):
        numItem += 1
        print (voltageTroyka)
        measure.append (voltageTroyka)
        voltageTroyka = voltage (adc ())

    finishTime = time.time ()
    duration = finishTime - startTime

    measureStr = [str(item) for item in measure]
    with open("data.txt", "w") as dataFile:
        dataFile.write ("\n".join(measureStr))

    with open("settings.txt", "w") as settingsFile:
        settingsFile.write ("продолжительность измерения: {:.3f} с\n".format(duration))
        settingsFile.write ("период измерения: {:.3f} с\n".format(duration / numItem))
        settingsFile.write ("частота дискретизации: {:.3f} Гц\n".format(numItem /  duration))
        settingsFile.write ("шаг квантования: {:.3f} В\n".format(MAXVOLT / 256))

    print ("продолжительность измерения: {:.3f} с".format(duration))
    print ("период измерения: {:.3f} с".format(duration / numItem))
    print ("частота дискретизации: {:.3f} Гц".format(numItem /  duration))
    print ("шаг квантования: {:.3f} В".format(MAXVOLT / 256))

    plot.plot (measure)
    plot.show ()

# заершение работы с GPIO
finally:
    GPIO.output (dac, 0)
    GPIO.output (troyka, 0)
    GPIO.output (leds, 0)

    GPIO.cleanup (dac)
    GPIO.cleanup (troyka)
    GPIO.cleanup (leds)

    