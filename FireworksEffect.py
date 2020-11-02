import argparse
from datetime import datetime
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


def fadeToBlackBy(color, fade):
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


def Palette256():
    # return (r,g,b)
    return Color(
        Random().randint(0,255),
        Random().randint(0,255),
        Random().randint(0,255)
    )


class Canvas():
    def __init__(self):
        # strip = None
        # self.DotCount = LED_COUNT
        # Create NeoPixel object with appropriate configuration.
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        self.DotCount = self.strip.numPixels()

    def FillSolid(self, color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)

    # def DrawPixels(self, position, size, color):
    #     dot = int(position)
    #     if dot < 0:return
    #     if dot >= self.DotCount:return
    #     # print("{dot:.2f}, {position:.2f}, {size:.2f}".format(dot=dot, position=position, size=size))
    #     self.strip.setPixelColor(dot, color)
    def DrawPixels(self, position, size, color):
        left_dot = int(position - size / 2)
        right_dot = int(position + size / 2)
        if right_dot < 0:return
        if left_dot < 0:
            left_dot = 0
        if left_dot >= self.DotCount:return
        if right_dot >= self.DotCount:
            right_dot = self.DotCount
        # print("{dot:.2f}, {position:.2f}, {size:.2f}".format(dot=dot, position=position, size=size))
        for dot in range(left_dot, right_dot + 1):
            self.strip.setPixelColor(dot, color)


class FireworksEffect():
    def __init__(self):
        self.Blend                  = True
        self.MaxSpeed               = 375.0 # Max velocity
        self.MaxSpeed               = 175.0 # Max velocity
        self.NewParticleProbability = 0.01  # Odds of new particle
        self.ParticlePreignitonTime = 0.0   # How long to "wink"
        self.ParticleIgnition       = 0.2   # How long to "flash"
        self.ParticleHoldTime       = 0.00  # Main lifecycle time
        self.ParticleFadeTime       = 2.0   # Fade out time
        self.ParticleSize           = 0.00  # Size of the particle
        self.particle_list          = []
        self._random                = Random()

    def render(self, graphics):
        # All drawing is done in Render, which produces one
        # frame by calling the draw methods on the supplied
        # graphics interface.  As long as you support "Draw
        # a pixel" you should be able to make it work with
        # whatever mechanism to plot pixels that you're using...

        # Randomly create some new stars this frame; the number we create is tied
        # to the size of the display so that the display size can change and
        # the "effect density" will stay the same
        for iPass in range(graphics.DotCount // 50):
            if self._random.random() < self.NewParticleProbability:
                # Pick a random color and location.
                # If you don't have FastLED palettes, all you need to do
                # here is generate a random color.

                iStartPos = self._random.random() * graphics.DotCount
                color = Palette256()
                c = self._random.randint(10, 50)
                multiplier = self._random.random() * 3

                for i in range(1, c):
                    particle = Particle(color, iStartPos, self.MaxSpeed * self._random.random() * multiplier)
                    self.particle_list.append(particle)

        # # In the degenerate case of particles not aging out for some reason,
        # # we need to set a pseudo-realistic upper bound, and the very number of
        # # possible pixels seems like a reasonable one
        while len(self.particle_list) > graphics.DotCount:
            self.particle_list = self.particle_list[1:]

        # Start out with an empty canvas
        graphics.FillSolid(black)

        for star in self.particle_list:
            star.Update()
            c = star._starColor

            # If the star is brand new, it flashes white briefly.
            # Otherwise it just fades over time.
            fade = 0.0
            if (star.Age() > self.ParticlePreignitonTime) and (star.Age() <
                            self.ParticleIgnition + self.ParticlePreignitonTime):
                c = white
            else:
                # Figure out how much to fade and shrink the star based on
                # its age relative to its lifetime
                age = star.Age()
                if (age < self.ParticlePreignitonTime):
                    fade = 1.0 - (age / self.ParticlePreignitonTime)
                else:
                    age -= self.ParticlePreignitonTime
                    if (age < self.ParticleHoldTime + self.ParticleIgnition):
                        fade = 0.0 # Just born
                    elif (age > self.ParticleHoldTime + self.ParticleIgnition + self.ParticleFadeTime):
                        fade = 1.0 # Black hole, all faded out
                    else:
                        age -= self.ParticleHoldTime + self.ParticleIgnition
                        fade = age / self.ParticleFadeTime  # Fading star
                c = fadeToBlackBy(c, fade)
            self.ParticleSize = (1 - fade) * 3

            # Because I support antialiasing and partial pixels, this takes a
            # non-integer number of pixels to draw.  But if you just made it
            # plot 'ParticleSize' pixels in int form, you'd be 99% of the way there
            graphics.DrawPixels(star._position, self.ParticleSize, c)

        # Remove any particles who have completed their lifespan
        while len(self.particle_list) > 0 and (self.particle_list[0].Age() >
            self.ParticleHoldTime + self.ParticleIgnition + self.ParticleFadeTime):
            self.particle_list = self.particle_list[1:]



class Particle():
    """Each particle in the particle system remembers its color,
    birth time, postion, velocity, etc.  If you are not using DateTime,
    all you need in its place is a fractional number of seconds elapsed, which is
    all I use it for.  So timer()/1000.0 or whatever should suffice as well."""

    def __init__(self, starColor, pos, maxSpeed):
        self._rand = Random()
        self._position = pos
        self._velocity = self._rand.random() * maxSpeed * 2 - maxSpeed
        self._starColor = starColor
        self._birthTime = datetime.utcnow()
        self._lastUpdate = datetime.utcnow()

    def Age(self):
        return (datetime.utcnow() - self._birthTime).total_seconds()

    def Update(self):
        # As the particle ages we actively fade its color and slow its speed
        deltaTime = (datetime.utcnow() - self._lastUpdate).total_seconds()
        self._position += self._velocity * deltaTime
        self._lastUpdate = datetime.utcnow()
        self._velocity -= (2 * self._velocity * deltaTime)
        self._starColor = fadeToBlackBy(self._starColor, self._rand.random() * 0.1)


if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    graphics = Canvas()
    fw = FireworksEffect()
    try:
        while True:
            fw.render(graphics)
            graphics.strip.show()
            time.sleep(10/1000)
    except KeyboardInterrupt:
        if args.clear:
            graphics.FillSolid(black)
            graphics.strip.show()
