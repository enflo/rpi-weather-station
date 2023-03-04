from src.settings import MQTT_HOST, MQTT_PORT, MQTT_TOPIC, MQTT_USER, MQTT_PASSWORD
import paho.mqtt.client as mqtt


class SendDataMQTT:
    def __init__(self, data):
        self.data = data

    def send(self):
        client = self._mqtt_client()
        self._publish(client, MQTT_TOPIC, self.data)
        client.disconnect()

    @staticmethod
    def _mqtt_client():
        client = mqtt.Client(transport="websockets")
        client.tls_set()
        client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
        client.connect(host=MQTT_HOST, port=MQTT_PORT, keepalive=60, bind_address="")
        return client

    @staticmethod
    def _publish(client, topic, payload):
        client.publish(topic, payload).wait_for_publish()
