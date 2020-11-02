# https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
import argparse
from random import Random
import time
from rpi_ws281x import PixelStrip, Color
from led_setup import *

def sparkle(strip, color=Color(255, 255, 255), sparkle_count=500, speed_delay=0):
    """
    strip = object rpi-ws281x PixelStrip
    color = object rpi-ws281x Color for the color of the eyes
    sparkle_count = int number of times to repeat a single sparkle
    speed_delay = int milliseconds between turning off one sparkle
    """
    FillSolid(strip, black)
    for i in range(sparkle_count):
        j = Random().randint(0, strip.numPixels())
        strip.setPixelColor(j, color)
        strip.show()
        time.sleep(speed_delay / 1000)
        strip.setPixelColor(j, black)
    strip.show()


if __name__ == '__main__':
    try:
        while True:
            sparkle(strip)
    except KeyboardInterrupt:
        FillSolid(strip, black)
        strip.show()
