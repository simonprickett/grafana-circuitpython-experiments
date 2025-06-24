from os import getenv

import board
import pwmio
import time
import wifi

ssid = getenv("CIRCUITPY_WIFI_SSID")
password = getenv("CIRCUITPY_WIFI_PASSWORD")

print(f"Connecting to {ssid}")
wifi.radio.connect(ssid, password)
print(f"Connected to {ssid}!")

gauge1 = pwmio.PWMOut(board.GP22, frequency=1000)
gauge2 = pwmio.PWMOut(board.GP26, frequency=1000)
gauge3 = pwmio.PWMOut(board.GP16, frequency=1000)

ds1 = 0
delta1 = 1000
ds2 = 65000
delta2 = -1000

while True:
    gauge1.duty_cycle = ds1
    gauge2.duty_cycle = ds2
    gauge3.duty_cycle = ds1
    
    ds1 = ds1 + delta1
    ds2 = ds2 + delta2

    if ds1 >= 65000:
        delta1 = -1000
    if ds1 <= 0:
        delta1 = 1000

    if ds2 >= 65000:
        delta2 = -1000
    if ds2 <= 0:
        delta2 = 1000

    time.sleep(0.05)