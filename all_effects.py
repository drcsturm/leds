# https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
import argparse
from random import Random
import time
from rpi_ws281x import PixelStrip, Color
from led_setup import *

import cylon
import halloween_eyes
import meteor
import running_lights
import sparkle
import strobe

if __name__ == "__main__":
    try:
        while True:
            print("Cylon")
            cylon.cylon_bounce(strip)
            print("Halloween Eyes")
            halloween_eyes.halloween_eyes(strip)
            print("Meteor Rain")
            meteor.meteor_rain(strip)
            print("Running Lights")
            running_lights.running_lights(strip)
            print("America Running Lights")
            running_lights.running_lights(strip, rperiod=1)
            print("Sparkle")
            sparkle.sparkle(strip)
            print("Strobe")
            strobe.strobe(strip)
    except KeyboardInterrupt:
        FillSolid(strip, black)
        strip.show()
        