#!/usr/bin/python3

# Program: LNX255 Assignment 2
# Student: Abdullah
# Date: April 11th, 2022

from smbus import SMBus
from gpiozero import PWMLED, Button
from signal import pause, signal, SIGTERM, SIGHUP
from time import sleep
from threading import Thread
from rpi_lcd import LCD
from math import log10

steps = 255
fade_factor = (steps * log10(2))/(log10(steps))
speed = 100
delay = 0.1
active = True
leds = [PWMLED(5), PWMLED(6), PWMLED(13), PWMLED(19), PWMLED(26)]
button = Button(22)
lcd = LCD()
bus = SMBus(1)
ads7830_commands = [0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4, 0x4b]


def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)


def cleanup(signum, frame):
    exit(1)


def change_speed():
    global delay
    global speed

    if speed == 100:
        speed = 80
    elif speed == 20:
        speed = 100
        delay = 0
    else:
        speed = speed - 20

    delay = delay + 0.1


def show_pattern():

    global brightness

    try:
        while active:
            for num in (0, 1, 2, 3, 4, 3, 2, 1):
                value = read_ads7830(0)
                brightness = (pow(2, (value/fade_factor))-1)/steps
                leds[num].value = brightness
                sleep(delay)
                leds[num].off()

    except AttributeError:
        pass


def display_brightness():
    global brightness
    global speed

    while active:
        Speed = f"Speed: {speed:2.0f}%"
        brightness1 = "Brightness: " + '{:2.0%}'.format(brightness)
        lcd.text(Speed, 1)
        lcd.text(brightness1, 2)
        sleep(0.1)


try:
    signal(SIGTERM, cleanup)
    signal(SIGHUP, cleanup)

    button.when_pressed = change_speed
    reader = Thread(target=show_pattern, daemon=True)
    display = Thread(target=display_brightness, daemon=True)
    reader.start()
    display.start()

    pause()

except KeyboardInterrupt:
    pass

finally:
    active = False
    reader.join()
    display.join()
    lcd.clear()
    for num in (0, 1, 2, 3, 4, 3, 2, 1):
        leds[num].close()
    sleep(0.25)
