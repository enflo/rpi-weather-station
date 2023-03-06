import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = Path('/home/pi/rpi-weather-station/.env')
print(dotenv_path)
load_dotenv(dotenv_path=dotenv_path)


ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOOP_TIME = int(os.getenv("LOOP_TIME", 1))

# API CONFIG
API_ENABLE = os.getenv("API_CONFIG", False)
API_METHOD = os.getenv("API_METHOD", "POST")
API_HOST = os.getenv("API_HOST", "localhost")
API_HEADER_TOKEN = os.getenv("API_HEADER_TOKEN", None)
API_URL_TOKEN = os.getenv("API_URL_TOKEN", "")

# MQTT CONFIG
MQTT_ENABLE = os.getenv("MQTT_ENABLE", False)
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "topic")
MQTT_USER = os.getenv("MQTT_USER", "user")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "password")
