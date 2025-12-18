import requests
from src.settings import SENSOR_COMMUNITY_SENSOR_SDS011_ID, SENSOR_COMMUNITY_SENSOR_BME280_ID


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
        requests.post(api_url, headers=header_pm, json=self.pm())
        # Enviar clima 
        requests.post(api_url, headers=headers_bme, json=self.bme())
        
    def pm(self):
        return {
            "P1": self.data["pm10"],
            "P2": self.data["pm25"],
        }

    def bme(self):
        return {
            "temperature": self.data["temperature_celsius"],
            "humidity": self.data["humidity"],
            "pressure": self.data["pressure"],
        }
