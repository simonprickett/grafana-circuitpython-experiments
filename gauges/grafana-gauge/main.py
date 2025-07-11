from gauge import Gauge
import adafruit_connection_manager
import adafruit_requests
import board
import os
import time
import wifi

g = Gauge(board.GP22)

print("Connecting to wifi...")

radio = wifi.radio
radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
              password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))

pool = adafruit_connection_manager.get_radio_socketpool(radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(radio)
requests = adafruit_requests.Session(pool, ssl_context)

print(f"Connected as {radio.ipv4_address}")

grafana_query = {
    "queries": [{
        "expr": "humidity{instance=\"kitchen\"}",
        "instant": True,
        "datasource": {
            "type": "prometheus",
            "uid": "grafanacloud-prom"
        },
        "utcOffsetSec": 3600
    }],
    "from": "0",
    "to": "now"
}

grafana_auth = {
    "Authorization": f"Bearer {os.getenv('GRAFANA_TOKEN')}"
}

while True:
    with requests.post(f"https://{os.getenv('GRAFANA_URL')}/api/ds/query", json=grafana_query, headers=grafana_auth) as response:
        resp = response.json()
        metric_value = resp["results"]["A"]["frames"][0]["data"]["values"][1][0]
        print(metric_value)

        g.set_percentage(metric_value, True)

    time.sleep(30)
