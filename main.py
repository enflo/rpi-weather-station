import time

from src.communication.send_data import send_data
from src.sensors.bme280sensor import BME280Sensor
from src.sensors.sds011 import SDS011Sensor
from src.settings import LOOP_TIME


def get_weather() -> dict:
    weather = {
        "timestamp": time.time(),
    }
    air_quality = SDS011Sensor().get_measurement()
    temperature_humidity_pressure = BME280Sensor().get_measurement()

    weather.update(air_quality)
    weather.update(temperature_humidity_pressure)

    return weather


if __name__ == "__main__":
    while True:
        result = get_weather()
        send_data(result)
        time.sleep(LOOP_TIME * 60)
