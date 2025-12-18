import os
from pathlib import Path

from dotenv import load_dotenv

# Look for .env file in the project root directory
project_root = Path(__file__).parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path)


def get_bool_env(key, default=False):
    """
    Get boolean environment variable.
    """
    value = os.getenv(key, default)
    if isinstance(value, bool):
        return value
    return str(value).lower() in ("true", "1", "yes", "on")


ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOOP_TIME = int(os.getenv("LOOP_TIME", 1))

# API CONFIG
API_ENABLE = get_bool_env("API_CONFIG", False)
API_METHOD = os.getenv("API_METHOD", "POST")
API_HOST = os.getenv("API_HOST", "localhost")
API_HEADER_TOKEN = os.getenv("API_HEADER_TOKEN", None)
API_URL_TOKEN = os.getenv("API_URL_TOKEN", "")

# MQTT CONFIG
MQTT_ENABLE = get_bool_env("MQTT_ENABLE", False)
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = os.getenv("MQTT_PORT", 1883)
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "topic")
MQTT_USER = os.getenv("MQTT_USER", "user")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "password")

# SQS CONFIG
SQS_ENABLE = get_bool_env("SQS_ENABLE", False)
SQS_URL = os.getenv("SQS_URL", "http://localhost:9324")
SQS_ACCESS_KEY = os.getenv("SQS_ACCESS_KEY", "access_key")
SQS_SECRET_KEY = os.getenv("SQS_SECRET_KEY", "secret_key")
SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", "queue_name")
SQS_REGION = os.getenv("SQS_REGION", "fr-par")


# POSTGRES CONFIG
POSTGRES_ENABLE = get_bool_env("POSTGRES_ENABLE", False)
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DBNAME = os.getenv("POSTGRES_DBNAME", "postgres")
POSTGRES_TABLE = os.getenv("POSTGRES_TABLE", "weather")
POSTGRES_SSLMODE = os.getenv("POSTGRES_SSLMODE", "prefer")
POSTGRES_CHANNELBINDING = os.getenv("POSTGRES_CHANNELBINDING", "prefer")


# SENSOR COMMUNITY CONFIG
SENSOR_COMMUNITY_ENABLE = get_bool_env("SENSOR_COMMUNITY_ENABLE", False)
SENSOR_COMMUNITY_SENSOR_ID = os.getenv("SENSOR_COMMUNITY_SENSOR_ID", "raspi-123456")
