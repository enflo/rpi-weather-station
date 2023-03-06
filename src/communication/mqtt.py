import json
import paho.mqtt.client as mqtt

from src.settings import MQTT_HOST, MQTT_PORT, MQTT_TOPIC, MQTT_USER, MQTT_PASSWORD


class SendDataMQTT:
    def __init__(self, data):
        self.data = data

    def send(self):
        client = self._mqtt_client()
        client.loop_start()
        self._publish(client, MQTT_TOPIC, self.data)
        client.disconnect()

    @staticmethod
    def _mqtt_client():
        client = mqtt.Client(transport="websockets")
        client.tls_set()
        client.username_pw_set("mqttrpi", "Toni240393")
        client.connect('mqtt.toniflorithomar.dev', 443, 30)
        return client

    @staticmethod
    def _publish(client, topic, payload):
        payload_string = json.dumps(payload)
        client.publish(topic, payload_string).wait_for_publish()
