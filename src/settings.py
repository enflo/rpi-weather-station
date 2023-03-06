import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = Path('../.env')
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
print(MQTT_ENABLE)
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
print(MQTT_HOST)
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
print(MQTT_PORT)
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "topic")
print(MQTT_TOPIC)
MQTT_USER = os.getenv("MQTT_USER", "user")
print(MQTT_USER)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "password")
print(MQTT_PASSWORD)
