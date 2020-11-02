# https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
import argparse
import math
from random import Random
import time
from rpi_ws281x import PixelStrip, Color
from led_setup import *

def running_lights(strip, color=Color(255, 255, 255),
    dynamic_color=False, wave_delay=50,
    rperiod=0.5, ramplitude=127, rshift=50,
    gperiod=0.5, gamplitude=127, gshift=50,
    bperiod=0.5, bamplitude=127, bshift=50,
    ):
    """
    strip = object rpi-ws281x PixelStrip
    color = object rpi-ws281x Color for the color of the eyes
    dynamic_color = boolean change the color of the waves every advance forward
    wave_delay = int milliseconds before moving wave forward

    To create a red white and blue sin wave use these settings:
        red   = 255, period = 1.0, shift = 50
        green = 255, period = 0.5, shift = 50
        blue  = 255, period = 0.5, shift = 50
    """

    def color_int(i, position, rgb, period=1, amplitude=127, shift=128):
        """
        i = int pixel along strip
        position = int how many times the wave has been moved forward
        period = float alter period of the wave
        amplitude = float alter the amplitude of the wave
        shift = float move the entire wave up or down relative to zero line
        """
        # val = int(round(((math.sin(i + position) * 127 + 128) / 255) * red, 0))
        # period = 1 # larger is shorter period, default = 1
        # amplitude = 127 # larger is bigger amplitude, default = 127
        # shift = 128 # higher moves entire wave up relative to zero line, default = 128
        val = int(round(((math.sin((i + position) * period) * amplitude + shift) / 255) * rgb, 0))
        # always return a value between 0 and 255
        if val < 0:
            return 0
        elif val > 255:
            return 255
        else:
            return val

    FillSolid(strip, black)
    red = (color & 0x00ff0000) >> 16
    green = (color & 0x0000ff00) >> 8
    blue = (color & 0x000000ff)
    position = 0
    for j in range(strip.numPixels() * 1):
        position += 1
        if dynamic_color:
            red = Random().randint(0, 255)
            green = Random().randint(0, 255)
            blue = Random().randint(0, 255)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(
                color_int(i, position, red, period=rperiod, amplitude=ramplitude, shift=rshift),
                color_int(i, position, green, period=gperiod, amplitude=gamplitude, shift=gshift),
                color_int(i, position, blue, period=bperiod, amplitude=bamplitude, shift=bshift)
            ))
        strip.show()
        time.sleep(wave_delay / 1000)


if __name__ == '__main__':
    try:
        while True:
            running_lights(strip)
            running_lights(strip, rperiod=1)
    except KeyboardInterrupt:
        FillSolid(strip, black)
        strip.show()
