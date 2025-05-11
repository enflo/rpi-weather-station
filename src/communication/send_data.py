from src.communication.api import SendDataAPI
from src.communication.mqtt import SendDataMQTT
from src.communication.postgres import SendDataPostgres
from src.communication.sqs import SQSClient
from src.settings import (
    API_ENABLE,
    MQTT_ENABLE,
    POSTGRES_ENABLE,
    SQS_ENABLE,
)


def send_data(data):
    """
    Intermediate method to send the information to API, MQTT, SQS, SupaBase, or PostgreSQL,
    otherwise just do a console print.
    """

    if API_ENABLE:
        SendDataAPI(data).send()
    elif MQTT_ENABLE:
        SendDataMQTT(data).send()
    elif SQS_ENABLE:
        SQSClient(data).send()
    elif POSTGRES_ENABLE:
        SendDataPostgres(data).send()
    else:
        print(data)
