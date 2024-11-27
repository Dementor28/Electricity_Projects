#!/usr/bin/python3

# Original Author: M. Heidenreich
# Adapted by: Abdullah
"""
    Program: Button-Operated Servo Motor (servo.py)
    Author:  M. Heidenreich, (c) 2020

    Description:
    
    This code is provided in support of the following YouTube tutorial:
    https://youtu.be/3tlE3fpryF0

    This example demonstrates how to implement a simple software-based button
    blocking/priority technique with Raspberry Pi GPIO and Python.
    The concept is demonstrated with a servo motor but can be applied
    in other settings as well. 

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL ARE PROVIDED "AS IS" AND THE
    AUTHOR DISCLAIMS ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""
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
