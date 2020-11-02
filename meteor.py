# https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
import argparse
from random import Random
import time
from rpi_ws281x import PixelStrip, Color
from led_setup import *

def meteor_rain(strip, color=Color(255, 255, 255), meteor_size=10, 
    meteor_trail_decay=0.25, random_decay=True, speed_delay=30):
    """
    strip = object rpi-ws281x PixelStrip
    color = object rpi-ws281x Color for the color of the eyes
    meteor_size = int for how many pixels wide the meteor is
    meteor_trail_decay = float 0 to 1, 0 is no fade, 1 is black, percent decay on each step
    random_decay = boolean True to make tail randomly decay or False to have a smooth fading line
    speed_delay = int milliseconds between meteor update
    """
    FillSolid(strip, black)
    for i in range(0, int(strip.numPixels() * 1)):

        # fade brightness of all LEDs by one step
        for j in range(0, strip.numPixels()):
            if ((not random_decay) or (Random().randint(0, 10) > 5)):
                temp_color = fadeToBlackBy(None, meteor_trail_decay, get_pixel_i_color=j)
                strip.setPixelColor(j, temp_color)
        # draw the meteor
        for j in range(0, meteor_size):
            if ( (i - j < strip.numPixels()) and (i - j >= 0) ):
                strip.setPixelColor(i - j, color)
        strip.show()
        time.sleep(speed_delay / 1000)


if __name__ == '__main__':
    try:
        while True:
            meteor(strip)
    except KeyboardInterrupt:
        FillSolid(strip, black)
        strip.show()
