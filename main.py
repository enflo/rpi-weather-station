import time

import board

from src.dht22 import TemperatureHumidityMonitor
from src.sds011 import AirQualityMonitor
import adafruit_dht


def get_weather(dht_connector) -> dict:
    weather = {
        "timestamp": time.time(),
    }
    air_quality = AirQualityMonitor().get_measurement()
    temperature_humidity = TemperatureHumidityMonitor(dht_connector).get_measurement()

    weather.update(air_quality)
    weather.update(temperature_humidity)

    return weather


if __name__ == "__main__":
    dht = adafruit_dht.DHT22(board.D4)
    while True:
        result = get_weather(dht)
        print(result)
        time.sleep(5)
