from os import getenv

import board
import pwmio
import time

MAX_DUTY_CYCLE = 60000

def percent_to_duty_cycle(pct):
    # Might as well do some sanity checks!
    if pct > 100:
        return MAX_DUTY_CYCLE
    elif pct == 0:
        return 0
    
    # What whole % of MAX_DUTY_CYCLE is pct?
    return int((pct / 100) * MAX_DUTY_CYCLE)


def set_gauge_to_percentage(gauge, pct):
    gauge.duty_cycle = percent_to_duty_cycle(pct)


gauge1 = pwmio.PWMOut(board.GP22, frequency=1000)

while True:
    set_gauge_to_percentage(gauge1, 33)
    time.sleep(2)

    set_gauge_to_percentage(gauge1, 66)
    time.sleep(2)

    set_gauge_to_percentage(gauge1, 100)
    time.sleep(2)

    set_gauge_to_percentage(gauge1, 66)
    time.sleep(2)

    set_gauge_to_percentage(gauge1, 33)
    time.sleep(2)

    set_gauge_to_percentage(gauge1, 0)
    time.sleep(2)