import math
import neopixel
import pwmio
import time

class Gauge:
    MIN_SLEEP = 0.01
    MAX_SLEEP = 0.04
    MAX_DUTY_CYCLE = 60000
    MAX_RGB_VALUE = 255

    def __init__(self, pin_gauge, pin_neopixels, num_neopixels, neopixel_brightness, red_high):
        self.gauge = pwmio.PWMOut(pin_gauge, frequency=1000)
        self.current_pct = 0
        self.red_high = red_high

        # TODO make the params for the pixels a dict and handle case where it is none.
        # TODO also add a parameter for whether 0% or 100% is the green end of the scale for the pixels.
        self.pixels = neopixel.NeoPixel(pin_neopixels, num_neopixels, brightness=neopixel_brightness, auto_write=True)
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

        # TODO provide a custom color function?


    def __percent_to_duty_cycle(self, pct):    
        return int((pct / 100) * self.MAX_DUTY_CYCLE)
    
    
    # Source from: https://gist.github.com/robweychert/7efa6a5f762207245646b16f29dd6671
    # Example web implementation at: https://codepen.io/ahopkins/pen/beNWWp
    def __easeInOutSine(self, t):
        return -(math.cos(math.pi * t) -1) / 2
    
    def __clip(self, num):
        return self.MAX_RGB_VALUE if num > self.MAX_RGB_VALUE else num


    def __get_red(self, i):
        percent = i / 100
        return self.__clip(percent * self.MAX_RGB_VALUE * 2)


    def __get_green(self, i):
        percent = i / 100
        return self.__clip((self.MAX_RGB_VALUE - (percent * self.MAX_RGB_VALUE)) * 2)


    def __get_color_for_pct(self, i):
        red = round(self.__get_red(i))
        green = round(self.__get_green(i))

        return (red, green, 0) if self.red_high == True else (green, red, 0)


    def set_percentage(self, new_pct, with_easing = False):
        if new_pct > 100:
            new_pct = 100
        elif new_pct < 0:
            new_pct = 0

        # If there's no change, do nothing.
        if new_pct == self.current_pct:
            return

        if with_easing == True:
            num_frames = abs(self.current_pct - new_pct)
            incr = -1 if new_pct < self.current_pct else 1

            for f in range(0, num_frames):
                easing = self.__easeInOutSine(f / num_frames)
                self.current_pct = self.current_pct + incr                
                self.gauge.duty_cycle = self.__percent_to_duty_cycle(self.current_pct)

                # Update the neopixels, if configured...
                # TODO only if there are some!
                self.pixels.fill(self.__get_color_for_pct(round(new_pct)))
                self.pixels.show()

                sleep_time = self.MIN_SLEEP + (self.MAX_SLEEP - self.MIN_SLEEP) * easing
                time.sleep(sleep_time)
                                
        else:
            self.gauge.duty_cycle = self.__percent_to_duty_cycle(new_pct)
            self.current_pct = new_pct

            # Update the neopixels, if configured...
            # TODO only if there are some!
            self.pixels.fill(self.__get_color_for_pct(round(new_pct)))
            self.pixels.show()