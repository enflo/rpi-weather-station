import logging
import requests
from src.settings import SENSOR_COMMUNITY_SENSOR_SDS011_ID, SENSOR_COMMUNITY_SENSOR_BME280_ID

logger = logging.getLogger(__name__)


class SendDataSensorCommunity:
    def __init__(self, data):
        self.data = data
        
    def send(self):
        api_url = "https://api.sensor.community/v1/push-sensor-data/"
        header_pm = {
            "X-PIN": "1",
            "X-Sensor": SENSOR_COMMUNITY_SENSOR_SDS011_ID,
            "Content-Type": "application/json"
        } 
        headers_bme = {
            "X-PIN": "11", # BME280
            "X-Sensor": SENSOR_COMMUNITY_SENSOR_BME280_ID,
            "Content-Type": "application/json"
        }
        # Enviar partículas
        try:
            logger.info("Sending PM data to Sensor Community")
            response_pm = requests.post(api_url, headers=header_pm, json=self.pm(), timeout=10)
            response_pm.raise_for_status()
            logger.info(f"PM data sent successfully: {response_pm.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending PM data: {e}")

        # Enviar clima 
        try:
            logger.info("Sending BME data to Sensor Community")
            response_bme = requests.post(api_url, headers=headers_bme, json=self.bme(), timeout=10)
            response_bme.raise_for_status()
            logger.info(f"BME data sent successfully: {response_bme.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending BME data: {e}")
        
    def pm(self):
        return {
            "software_version": "rpi-weather-station-1.0",
            "sensordatavalues": [
                {"value_type": "P1", "value": self.data["pm10"]},
                {"value_type": "P2", "value": self.data["pm25"]},
            ]
        }

    def bme(self):
        return {
            "software_version": "rpi-weather-station-1.0",
            "sensordatavalues": [
                {"value_type": "temperature", "value": self.data["temperature_celsius"]},
                {"value_type": "humidity", "value": self.data["humidity"]},
                {"value_type": "pressure", "value": self.data["pressure"]},
            ]
        }
