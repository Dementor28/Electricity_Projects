#!/usr/bin/python3

from signal import signal, SIGTERM, SIGHUP, pause
from time import sleep
from threading import Thread
from gpiozero import DistanceSensor, LED, Buzzer, Device
from gpiozero.pins.pigpio import PiGPIOFactory

Device.pin_factory = PiGPIOFactory()

reading = True
sensor = DistanceSensor(echo=20, trigger=21)
buzzer = Buzzer(24)

led1 = LED(18)
led2 = LED(23)
led3 = LED(25)


def safe_exit(signum, frame):
    exit(1)


def read_distance():
    global message

    while reading:
        message = f"Distance: {sensor.value*100:2.2f} cm"
        print(message)
        sleep(0.1)

        if sensor.value > 0.20:
            led1.on()
            led2.off()
            led3.off()
            buzzer.off()

        elif sensor.value < 0.20 and sensor.value > 0.05:
            led2.on()
            led1.off()
            led3.off()
            buzzer.toggle()

        else:
            led3.on()
            led1.off()
            led2.off()
            buzzer.on()


try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    reader = Thread(target=read_distance, daemon=True)
    reader.start()

    pause()

except KeyboardInterrupt:
    pass

finally:
    reading = False
    reader.join()
    sensor.close()
    led1.close()
    led2.close()
    led3.close()
    buzzer.close()
