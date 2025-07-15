from gauge import Gauge
import board
import time

g = Gauge(pin_gauge=board.GP22, pin_neopixels=board.GP2, num_neopixels=2, neopixel_brightness=0.02, red_high=True)

while True:
    for pct in range (0, 101, 5):
        g.set_percentage(pct, True)
        time.sleep(0.1)

    time.sleep(2)

    for pct in range (100, -1, -5):
        g.set_percentage(pct, True)
        time.sleep(0.1)

    time.sleep(2)
