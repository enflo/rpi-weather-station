import json

import boto3
from src.settings import SQS_REGION, SQS_QUEUE_NAME, SQS_URL, SQS_ACCESS_KEY, SQS_SECRET_KEY


class SQSClient:

    def __init__(self, data):
        self.data = data

    def send(self):
        queue = self._get_queue()
        self._publish(queue, self.data)

    @staticmethod
    def _sqs_client():
        print(SQS_ACCESS_KEY, SQS_SECRET_KEY)
        return boto3.resource(
            'sqs',
            endpoint_url=SQS_URL,
            aws_access_key_id=SQS_ACCESS_KEY,
            aws_secret_access_key=SQS_SECRET_KEY,
            region_name=SQS_REGION,
        )

    def _get_queue(self):
        return self._sqs_client().get_queue_by_name(QueueName=SQS_QUEUE_NAME)

    @staticmethod
    def _publish(queue, payload) -> None:
        str_json_payload = json.loads(payload)
        response = queue.send_message(MessageBody=str_json_payload)
        print(response.get('MessageId'))
        print(response.get('MD5OfMessageBody'))
