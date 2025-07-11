import math
import pwmio
import time

class Gauge:
    MIN_SLEEP = 0.01
    MAX_SLEEP = 0.04
    MAX_DUTY_CYCLE = 60000

    def __init__(self, pin):
        self.gauge = pwmio.PWMOut(pin, frequency=1000)
        self.current_pct = 0


    def __percent_to_duty_cycle(self, pct):    
        return int((pct / 100) * self.MAX_DUTY_CYCLE)
    
    
    # Source from: https://gist.github.com/robweychert/7efa6a5f762207245646b16f29dd6671
    def __easeInOutSine(self, t):
        return -(math.cos(math.pi * t) -1) / 2


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

                sleep_time = self.MIN_SLEEP + (self.MAX_SLEEP - self.MIN_SLEEP) * easing
                time.sleep(sleep_time)
                                
        else:
            self.gauge.duty_cycle = self.__percent_to_duty_cycle(new_pct)
            self.current_pct = new_pct