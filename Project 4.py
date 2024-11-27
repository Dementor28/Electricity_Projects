#!/usr/bin/python3
# To enable server deamon use sudo systemctl start pigpiod

from signal import signal, SIGTERM, SIGHUP, pause
from gpiozero import Servo, Button, Device, PWMLED
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
from math import log10

Device.pin_factory = PiGPIOFactory()

def safe_exit(signum, frame):
    exit(1)

def move_left():
    if left.held_time > (right.held_time or 0):
        if servo.value > -0.99 and LED.value > 0.01:
            servo.value -= 0.01
            LED.value -= 0.01

def move_right():
    if right.held_time > (left.held_time or 0):
        if servo.value < 0.99 and LED.value < 0.99:
            servo.value += 0.01
            LED.value += 0.01
        else:
            LED.blink(0.12, 0.05)

LED = PWMLED(13, initial_value=0.5)
servo = Servo(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
left = Button(16, hold_time=0.01, hold_repeat=True)
right = Button(20, hold_time=0.01, hold_repeat=True)

try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    LED.value = (servo.value+1)/2

    left.when_held = move_left
    right.when_held = move_right

    pause()

except KeyboardInterrupt:
    pass

finally:
    servo.mid()
    sleep(0.5)
    servo.close()
    LED.close()
