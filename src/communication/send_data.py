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


def send_data(data):
    """
    Intermediate method to send the information to API, MQTT, SQS, SupaBase, or PostgreSQL,
    otherwise just do a console print.
    """

    if API_ENABLE:
        SendDataAPI(data).send()
    if MQTT_ENABLE:
        SendDataMQTT(data).send()
    if SQS_ENABLE:
        SQSClient(data).send()
    if POSTGRES_ENABLE:
        SendDataPostgres(data).send()
    if SENSOR_COMMUNITY_ENABLE:
        SendDataSensorCommunity(data).send()
    
    print(data)
