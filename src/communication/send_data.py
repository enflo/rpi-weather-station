from src.settings import API_ENABLE, MQTT_ENABLE
from src.communication.api import SendDataAPI
from src.communication.mqtt import SendDataMQTT


def send_data(data):
    """
    Intermediate method to send the information to API or MQTT, otherwise just do a console print.
    """

    if API_ENABLE:
        print('api enabled')
        SendDataAPI(data).send()

    if MQTT_ENABLE:
        print('mqtt enabled')
        SendDataMQTT(data).send()

    print('console print')
    print(data)
