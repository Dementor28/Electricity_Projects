#!/usr/bin/python3

from gpiozero import LED, Button
from signal import signal, SIGTERM, SIGHUP, pause
from time import sleep


def safe_exit(signum, frame):
    exit(1)


time_on = 1
time_off = 2
time_off1 = 3


blink_on = False

def go_blink():
    global blink_on

    if blink_on:
        led1.off()
        led2.off()
        led3.off()
    else:
        led1.blink(time_on, time_off1)
        sleep(time_on)
        led2.blink(time_on, time_on)
        sleep(time_on)
        led3.blink(time_on, time_off1)


    blink_on = not blink_on

button = Button(21)

led1 = LED(13)
led2 = LED(19)
led3 = LED(26)


try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    button.when_pressed = go_blink

    pause()
except KeyboardInterrupt:
    pass


finally: 
    pass
