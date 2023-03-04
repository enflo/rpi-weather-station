import time
from src.sensors.dht22 import TemperatureHumidityMonitor
from src.sensors.sds011 import AirQualityMonitor
from src.settings import LOOP_TIME
from src.communication.send_data import send_data


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
        send_data(result)
        time.sleep(LOOP_TIME * 60)
