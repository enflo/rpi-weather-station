from src.settings import API_ENABLE, MQTT_ENABLE
from api import SendDataAPI
from mqtt import SendDataMQTT


def send_data(data):
    """
    Intermediate method to send the information to API or MQTT, otherwise just do a console print.
    """

    if API_ENABLE:
        SendDataAPI(data).send()

    if MQTT_ENABLE:
        SendDataMQTT(data).send()

    print(data)
