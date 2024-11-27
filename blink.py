#!/usr/bin/python3

from gpiozero import LED
from signal import pause
from time import sleep

led1 = LED(13)
led2 = LED(19)
led3 = LED(26)

try:
    led1.blink(1,3)
    sleep(1)
    led2.blink(1,1)
    sleep(1)
    led3.blink(1,3)

    pause()

except KeyboardInterrupt:
    pass
