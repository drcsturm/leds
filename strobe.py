# https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
import argparse
from random import Random
import time
from rpi_ws281x import PixelStrip, Color
from led_setup import *

def strobe(strip, color=Color(255, 255, 255), strobe_count=10, 
    flash_delay=50, repeat_delay=1000):
    """
    strip = object rpi-ws281x PixelStrip
    color = object rpi-ws281x Color for the color of the eyes
    strobe_count = int number of times to flash
    flash_delay = int milliseconds between flashes
    repeat_delay = int milliseconds before restarting
    """
    for i in range(strobe_count):
        FillSolid(strip, color)
        strip.show()
        time.sleep(flash_delay / 1000)
        FillSolid(strip, black)
        strip.show()
        time.sleep(flash_delay / 1000)
    time.sleep(repeat_delay / 1000)


if __name__ == '__main__':
    try:
        while True:
            strobe(strip)
    except KeyboardInterrupt:
        FillSolid(strip, black)
        strip.show()
