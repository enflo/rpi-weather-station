from src.dht22 import TemperatureHumidityMonitor
from src.sds011 import AirQualityMonitor


if __name__ == "__main__":
    air_quality = AirQualityMonitor().get_measurement()
    temperature_humidity = TemperatureHumidityMonitor().get_measurement()
    print(air_quality)
    print(temperature_humidity)
