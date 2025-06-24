import board
import pwmio
import time

# Assumes a Raspberry Pi Pico 2 W, with gauge connected
# to GP22 / Pin 29 and ground.  Sweeps the gauge back and
# forth on a continuous timer.

gauge = pwmio.PWMOut(board.GP22, frequency=1000)

ds = 0
delta = 1000

while True:
    print(ds)
    gauge.duty_cycle = ds

    ds = ds + delta

    if ds >= 65000:
        delta = -1000
    if ds <= 0:
        delta = 1000

    time.sleep(0.05)
