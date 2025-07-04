from gauge import Gauge
import board
import time

g = Gauge(board.GP22)

while True:
    g.set_percentage(33)
    time.sleep(2)

    g.set_percentage(66)
    time.sleep(2)

    g.set_percentage(100)
    time.sleep(2)

    g.set_percentage(66)
    time.sleep(2)

    g.set_percentage(33)
    time.sleep(2)

    g.set_percentage(0)
    time.sleep(2)