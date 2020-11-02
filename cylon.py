# https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
import argparse
from random import Random
import time
from rpi_ws281x import PixelStrip, Color
from led_setup import *

def cylon_bounce(strip, color=Color(255, 0, 0), eyesize=4, 
    speed_delay=10, return_delay=50):
    """
    strip = object rpi-ws281x PixelStrip
    color = object rpi-ws281x Color for the color of the eyes
    eyesize = int for how many pixels wide each eye is
    speed_delay = int how many milliseconds to delay moving the eye, higher is slower
    return_delay = int how many milliseconds to delay bouncing the eye, higher is slower
    """

    for i in range(0, strip.numPixels() - eyesize - 2):
        FillSolid(strip, black)
        strip.setPixelColor(i, fadeToBlackBy(color, 0.9))
        for j in range(0, eyesize):
            strip.setPixelColor(i + j + 1, color)
        strip.setPixelColor(i + eyesize + 1, fadeToBlackBy(color, 0.9))
        strip.show()
        time.sleep(speed_delay / 1000)
    time.sleep(return_delay / 1000)
    for i in range(strip.numPixels() - eyesize - 2, 0, -1):
        FillSolid(strip, black)
        strip.setPixelColor(i, fadeToBlackBy(color, 0.9))
        for j in range(0, eyesize):
            strip.setPixelColor(i + j + 1, color)
        strip.setPixelColor(i + eyesize + 1, fadeToBlackBy(color, 0.9))
        strip.show()
        time.sleep(speed_delay / 1000)
    time.sleep(return_delay / 1000)


if __name__ == '__main__':
    try:
        while True:
            cylon_bounce(strip)
    except KeyboardInterrupt:
        FillSolid(strip, black)
        strip.show()
