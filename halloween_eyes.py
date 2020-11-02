# https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
import argparse
from random import Random
import time
from rpi_ws281x import PixelStrip, Color
from led_setup import *

def halloween_eyes(strip, color=Color(255, 0, 0), eyewidth=1, eyespace=2, 
    fade=True, fade_steps=Random().randint(5, 30),
    fade_time=Random().randint(500, 1500),
    repeat_delay=Random().randint(1000, 4000)):
    """
    strip = object rpi-ws281x PixelStrip
    color = object rpi-ws281x Color for the color of the eyes
    eyewidth = int for how many pixels wide each eye is
    eyespace = int for how many pixels apart each eye is
    fade = boolean fade eyes
    fade_steps = number of steps to fade eyes (10)
    fade_time = total fade time in milliseconds until eyes are gone (1000)
    repeat_delay = int milliseconds before showing new eyes (3000)
    """
    FillSolid(strip, black)

    start_eye1 = Random().randint(0, strip.numPixels() - (2 * eyewidth) - eyespace)
    start_eye2 = start_eye1 + eyewidth + eyespace

    for i in range(0, eyewidth):
        strip.setPixelColor(start_eye1 + i, color)
        strip.setPixelColor(start_eye2 + i, color)
    strip.show()

    if fade:
        fade_delay = fade_time / fade_steps / 1000
        for j in range(fade_steps, 0, -1):
            fade_percent = 1.0 - (j -1) / fade_steps
            faded_color = fadeToBlackBy(color, fade_percent)

            for i in range(0, eyewidth):
                strip.setPixelColor(start_eye1 + i, faded_color)
                strip.setPixelColor(start_eye2 + i, faded_color)
            strip.show()
            time.sleep(fade_delay)
    time.sleep(repeat_delay / 1000)


if __name__ == '__main__':
    try:
        while True:
            halloween_eyes(strip)
    except KeyboardInterrupt:
        FillSolid(strip, black)
        strip.show()
