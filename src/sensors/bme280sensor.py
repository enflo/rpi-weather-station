import adafruit_bme280.advanced as adafruit_bme280
import board

from src.utils import celsius_to_fahrenheit


class BME280Sensor:
    def __init__(self):
        self.address = 0x77
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=self.address)
        # Configure the sensor for higher accuracy
        self.sensor.sea_level_pressure = 1013.25  # Standard sea level pressure in hPa
        self.sensor.mode = adafruit_bme280.MODE_NORMAL
        self.sensor.standby_period = adafruit_bme280.STANDBY_TC_500
        self.sensor.iir_filter = adafruit_bme280.IIR_FILTER_X16
        self.sensor.overscan_pressure = adafruit_bme280.OVERSCAN_X16
        self.sensor.overscan_humidity = adafruit_bme280.OVERSCAN_X1
        self.sensor.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    def get_measurement(self):
        return {
            "sensor_temp_hum": "bme280",
            "temperature_farenheit": celsius_to_fahrenheit(self.sensor.temperature),
            "temperature_celsius": self.sensor.temperature,
            "humidity": self.sensor.humidity,
            "pressure": self.sensor.pressure,
        }

    def _get_data(self):
        # This method is kept for compatibility but is no longer needed
        # as we can access sensor data directly through properties
        return self.sensor
