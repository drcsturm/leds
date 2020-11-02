# https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
import argparse
import math
from random import Random
import time
from rpi_ws281x import PixelStrip, Color


# LED strip configuration:
LED_COUNT = 150        # Number of LED pixels.
LED_COUNT = 300        # Number of LED pixels.
LED_COUNT = 150 + 65        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_BRIGHTNESS = 180  # Set to 0 for darkest and 255 for brightest
LED_BRIGHTNESS = 60   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# black = (0,0,0)
# white = (255,255,255)
black = Color(0,0,0)
white = Color(255,255,255)


def fadeToBlackBy(color, fade, get_pixel_i_color=None):
    """
    color = object rpi_ws281x Color
    fade = float between 0 and 1, 0 = no fade, 1= full black faded
    return Color that is faded
    """
    if isinstance(get_pixel_i_color, int):
        color = strip.getPixelColor(get_pixel_i_color)
    # return color
    fade = int(fade * 256)
    r = (color & 0x00ff0000) >> 16
    g = (color & 0x0000ff00) >> 8
    b = (color & 0x000000ff)
    if (r<=10):
        r = 0;
    else:
        r = r - (r * fade // 256)
    if (g<=10):
        g = 0;
    else:
        g = g - (g * fade // 256)
    if (b<=10):
        b = 0;
    else:
        b = b - (b * fade // 256)
    return Color(r, g, b)


def FillSolid(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)


def halloween_eyes(strip, color=Color(255, 0, 0), eyewidth=1, eyespace=2, 
    fade=True, fade_steps=10, fade_time=1000, repeat_delay=3000):
    """
    strip = object rpi-ws281x PixelStrip
    color = object rpi-ws281x Color for the color of the eyes
    eyewidth = int for how many pixels wide each eye is
    eyespace = int for how many pixels apart each eye is
    fade = boolean fade eyes
    fade_steps = number of steps to fade eyes
    fade_time = total fade time in milliseconds until eyes are gone
    repeat_delay = int milliseconds before showing new eyes
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


def cylon_bounce(strip, color=Color(255, 0, 0), eyesize=4, speed_delay=10, return_delay=50):
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


def meteor_rain(strip, color=Color(255, 255, 255), meteor_size=10, meteor_trail_decay=0.25, random_decay=True, speed_delay=30):
    """
    strip = object rpi-ws281x PixelStrip
    color = object rpi-ws281x Color for the color of the eyes
    meteor_size = int for how many pixels wide the meteor is
    meteor_trail_decay = float 0 to 1, 0 is no fade, 1 is black, percent decay on each step
    random_decay = boolean True to make tail randomly decay or False to have a smooth fading line
    speed_delay = int milliseconds between meteor update
    """
    FillSolid(strip, black)
    for i in range(0, int(strip.numPixels() * 1.5)):

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


def strobe(strip, color=Color(255, 255, 255), strobe_count=10, flash_delay=50, repeat_delay=1000):
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


def running_lights(strip, red=255, green=255, blue=255, wave_count=100, wave_delay=50):
    FillSolid(strip, black)
    for k in range(wave_count):
        position = 0
        for j in range(strip.numPixels() * 2):
            position += 1
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(
                    int(round(((math.sin(i + position) * 127 + 128) / 255) * red, 0)),
                    int(round(((math.sin(i + position) * 127 + 128) / 255) * green, 0)),
                    int(round(((math.sin(i + position) * 127 + 128) / 255) * blue, 0))
                ))
            strip.show()
            time.sleep(wave_delay / 1000)



# Main program logic follows
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            halloween_eyes(strip)
            halloween_eyes(strip, color=Color(255, 0, 0), eyewidth=1, eyespace=2, 
                fade=True, fade_steps=Random().randint(5, 30), 
                fade_time=Random().randint(500, 1500), 
                repeat_delay=Random().randint(1000, 4000))
            cylon_bounce(strip)
            meteor_rain(strip)
            strobe(strip)
            sparkle(strip)
            running_lights(strip)
    except KeyboardInterrupt:
        if args.clear:
            FillSolid(strip, black)
            strip.show()
