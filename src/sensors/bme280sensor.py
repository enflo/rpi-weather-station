import bme280
import smbus2


class BME280Sensor:
    def __init__(self):
        self.port = 1
        self.address = 0x77
        self.bus = smbus2.SMBus(self.port)

    def get_measurement(self):
        bme280_data = self._get_data()
        return {
            "sensor_temp_hum": "bme280",
            "temperature_farenheit": bme280_data.temperature * (9 / 5) + 32,
            "temperature_celsius": bme280_data.temperature,
            "humidity": bme280_data.humidity,
            "pressure": bme280_data.pressure,
        }

    def _get_data(self):
        bme280.load_calibration_params(self.bus, self.address)
        bme280_data = bme280.sample(self.bus, self.address)
        return bme280_data
