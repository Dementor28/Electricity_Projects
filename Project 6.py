#!/usr/bin/python3

"""
    Program:        Analog Joystick Tutorial (joystick.py)
    Author:         M. Heidenreich, (c) 2021
    Description:    This code is provided in support
                    of the following YouTube tutorial:
                    https://youtu.be/fX225p-Sh58

    This tutorial demonstrates how to use an analog joystick
    with Raspberry Pi and Python,
    including how to compensate for drift.

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL ARE PROVIDED "AS IS"
    AND THE AUTHOR DISCLAIMS
    ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES
    OF MERCHANTABILITY AND FITNESS.
    IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
    SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
    OR ANY DAMAGES WHATSOEVER RESULTING FROM
    LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
    CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from signal import signal, SIGTERM, SIGHUP, pause
from smbus import SMBus
from gpiozero import PWMLED
from time import sleep

bus = SMBus(1)
ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)


top = PWMLED(6)
right = PWMLED(26)
bottom = PWMLED(19)
left = PWMLED(13)


def safe_exit(signum, frame):
    exit(1)


def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)


def no_drift(input):
    value = read_ads7830(input)
    return value if value < 110 or value > 140 else 127


def read_min(input):
    while True:
        value = read_ads7830(input)

        yield (127-value)/127 if value < 110 else 0


def read_max(input):
    while True:
        value = read_ads7830(input)

        yield (value-128)/127 if value > 140 else 0


try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    top.source = read_max(6)
    right.source = read_max(7)
    bottom.source = read_min(6)
    left.source = read_min(7)

    pause()

except KeyboardInterrupt:
    pass

finally:
    top.source = None
    right.source = None
    bottom.source = None
    left.source = None
    top.close()
    right.close()
    bottom.close()
    left.close()
