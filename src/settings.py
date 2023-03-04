import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.', '.env')
load_dotenv(dotenv_path=env_path)

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# API CONFIG
API_ENABLE = os.getenv("API_CONFIG", False)
API_METHOD = os.getenv("API_METHOD", "POST")
API_HOST = os.getenv("API_HOST", "localhost")
API_HEADER_TOKEN = os.getenv("API_HEADER_TOKEN", None)
API_URL_TOKEN = os.getenv("API_URL_TOKEN", "")

# MQTT CONFIG
MQTT_ENABLE = os.getenv("MQTT_ENABLE", False)
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = os.getenv("MQTT_PORT", 1883)
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "topic")
MQTT_USER = os.getenv("MQTT_USER", "user")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "password")
