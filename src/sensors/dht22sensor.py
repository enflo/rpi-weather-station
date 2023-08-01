import time

import adafruit_dht
import board


class DHT22Sensor:
    def __init__(self):
        self.dht = adafruit_dht.DHT22(board.D4, False)

    def get_measurement(self):
        temperature_f, temperature_c, humidity = self.get_temperature_humidity()
        return {
            "sensor_temp_hum": "dht22",
            "temperature_farenheit": temperature_f,
            "temperature_celsius": temperature_c,
            "humidity": humidity,
        }

    def get_temperature_humidity(self):
        temperature_c = None
        temperature_f = None
        humidity = None
        try:
            temperature_c = self.dht.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = self.dht.humidity
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
        except Exception as error:
            print(error)
        return temperature_f, temperature_c, humidity
