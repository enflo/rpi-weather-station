import time

from src.dht22 import TemperatureHumidityMonitor
from src.sds011 import AirQualityMonitor


def get_weather() -> dict:
    weather = {
        "timestamp": time.time(),
    }
    air_quality = AirQualityMonitor().get_measurement()
    temperature_humidity = TemperatureHumidityMonitor().get_measurement()

    weather.update(air_quality)
    weather.update(temperature_humidity)

    return weather


if __name__ == "__main__":
    while True:
        result = get_weather()
        print(result)
        time.sleep(5)
