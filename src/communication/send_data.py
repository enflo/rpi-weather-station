import logging

from src.communication.api import SendDataAPI
from src.communication.mqtt import SendDataMQTT
from src.communication.postgres import SendDataPostgres
from src.communication.sqs import SQSClient
from src.communication.sensor_community import SendDataSensorCommunity
from src.settings import (
    API_ENABLE,
    MQTT_ENABLE,
    POSTGRES_ENABLE,
    SQS_ENABLE,
    SENSOR_COMMUNITY_ENABLE,
)

logger = logging.getLogger(__name__)


def send_data(data):
    """
    Intermediate method to send the information to API, MQTT, SQS, SupaBase, or PostgreSQL,
    otherwise just do a console print.
    """

    if API_ENABLE:
        try:
            SendDataAPI(data).send()
        except Exception as e:
            logger.error(f"Failed to send data to API: {e}")

    if MQTT_ENABLE:
        try:
            SendDataMQTT(data).send()
        except Exception as e:
            logger.error(f"Failed to send data to MQTT: {e}")

    if SQS_ENABLE:
        try:
            SQSClient(data).send()
        except Exception as e:
            logger.error(f"Failed to send data to SQS: {e}")

    if POSTGRES_ENABLE:
        try:
            SendDataPostgres(data).send()
        except Exception as e:
            logger.error(f"Failed to send data to Postgres: {e}")

    if SENSOR_COMMUNITY_ENABLE:
        try:
            SendDataSensorCommunity(data).send()
        except Exception as e:
            logger.error(f"Failed to send data to Sensor Community: {e}")
    
    logger.info(f"Data processed: {data}")
