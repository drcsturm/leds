# https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
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

black = Color(0,0,0)
white = Color(255,255,255)

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, 
    LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()


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


