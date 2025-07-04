import pwmio

class Gauge:
    MAX_DUTY_CYCLE = 60000

    def __init__(self, pin):
        self.gauge = pwmio.PWMOut(pin, frequency=1000)
        self.current_pct = 0


    def __percent_to_duty_cycle(self, pct):    
        return int((pct / 100) * self.MAX_DUTY_CYCLE)


    def set_percentage(self, new_pct, smooth_transition = False):
        if new_pct > 100:
            new_pct = 100
        elif new_pct < 0:
            new_pct = 0

        if smooth_transition == True:
            print("TODO smooth transitions!")
        else:
            self.gauge.duty_cycle = self.__percent_to_duty_cycle(new_pct)

        self.current_pct = new_pct
        

