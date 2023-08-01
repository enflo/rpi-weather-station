from src.communication.api import SendDataAPI
from src.communication.mqtt import SendDataMQTT
from src.settings import API_ENABLE, MQTT_ENABLE


def send_data(data):
    """
    Intermediate method to send the information to API or MQTT, otherwise just do a console print.
    """

    if API_ENABLE:
        SendDataAPI(data).send()
    elif MQTT_ENABLE:
        SendDataMQTT(data).send()
    elif NATS_ENABLE:
        SendDataNATS(data).send()
    else:
        print(data)
